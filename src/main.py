"""CLI entry point for the Capybara World Travel KDP pipeline.

Usage examples:
  python3 src/main.py --book tokyo
  python3 src/main.py --book tokyo --provider gemini
  python3 src/main.py --book tokyo --skip-images
  python3 src/main.py --all
  python3 src/main.py --rename tokyo
  python3 src/main.py --refresh-prompts
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

import pandas as pd

# Load .env from project root if it exists (keeps API keys out of the shell history)
_ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
if _ENV_FILE.exists():
    for _line in _ENV_FILE.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

from asset_renamer import rename_png_pages, slugify
from book_loader import load_book_record, find_row_for_slug
from config import (
    CONFIG,
    COVERS_ROOT,
    DEFAULT_IMAGE_PROVIDER,
    IMAGE_MARGIN,
    LOGS_ROOT,
    OUTPUT_COVERS,
    OUTPUT_INTERIORS,
    OUTPUT_KDP_READY,
    OUTPUT_METADATA,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    PAGES_PER_BOOK,
    PAGES_ROOT,
    RAW_DOWNLOADS_ROOT,
    SPREADSHEET_PATH,
    STORYBOARD_CACHE_DIR,
)
from image_utils import find_png_pages
from pdf_builder import build_interior_pdf
from spreadsheet_prompts import refresh_prompt_columns


def setup_logging() -> None:
    LOGS_ROOT.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_ROOT / "pipeline.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def main() -> None:
    setup_logging()
    args = parse_args()

    if args.rename:
        rename_downloaded_pages(args)
        return

    if args.refresh_prompts:
        refresh_spreadsheet_prompts(args)
        return

    if args.book:
        run_pipeline_for_book(args.book, args)
        return

    if args.all:
        run_pipeline_for_all_books(args)
        return

    # Default (no flags): build interior PDF from existing pages — legacy behaviour
    generate_interior_pdf()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capybara World Travel — fully automated KDP coloring book pipeline.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    pipeline = parser.add_argument_group("pipeline")
    pipeline.add_argument(
        "--book",
        metavar="BOOK_SLUG",
        help="Run the full generation pipeline for one book (e.g. --book tokyo).",
    )
    pipeline.add_argument(
        "--all",
        action="store_true",
        help="Run the full pipeline for every row in the spreadsheet.",
    )
    pipeline.add_argument(
        "--provider",
        default=DEFAULT_IMAGE_PROVIDER,
        choices=["stub", "gemini", "pollinations", "openai", "huggingface", "ideogram"],
        help="Image generation backend. 'stub' creates placeholder PNGs without any API. "
             "(default: %(default)s, or set IMAGE_PROVIDER env var)",
    )
    pipeline.add_argument(
        "--skip-images",
        action="store_true",
        help="Skip image generation and assemble PDF from pages that already exist on disk.",
    )
    pipeline.add_argument(
        "--skip-cover",
        action="store_true",
        help="Skip cover image generation (use existing cover) but still generate interior pages.",
    )
    pipeline.add_argument(
        "--workers",
        type=int,
        default=1,
        metavar="N",
        help="Parallel image generation workers (default: 1). Use 3-5 for Pollinations.ai.",
    )

    utils = parser.add_argument_group("asset utilities")
    utils.add_argument(
        "--rename",
        metavar="BOOK_SLUG",
        help="Rename raw downloaded PNGs into sequential page names (e.g. --rename tokyo).",
    )
    utils.add_argument(
        "--raw-dir",
        type=Path,
        help="Raw PNG source folder for --rename. Defaults to assets/raw_downloads/<slug>/.",
    )
    utils.add_argument(
        "--copy",
        action="store_true",
        help="Copy files instead of moving them during --rename.",
    )
    utils.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing sequential PNGs during --rename.",
    )
    utils.add_argument(
        "--refresh-prompts",
        action="store_true",
        help="Regenerate prompt columns in the automation spreadsheet.",
    )
    utils.add_argument(
        "--spreadsheet",
        type=Path,
        default=SPREADSHEET_PATH,
        help="Spreadsheet to read from or update. (default: %(default)s)",
    )
    utils.add_argument(
        "--output-spreadsheet",
        type=Path,
        help="Output workbook for --refresh-prompts. Defaults to overwriting the input file.",
    )
    return parser.parse_args()


# ── Full pipeline ──────────────────────────────────────────────────────────────

def run_pipeline_for_book(
    book_slug: str,
    args: argparse.Namespace,
    row_index: int = 0,
) -> None:
    from cover_builder import build_cover_pdf
    from image_gen import get_provider
    from metadata_gen import generate_metadata, save_metadata
    from storyboard import generate_storyboard

    log = logging.getLogger(__name__)
    slug = slugify(book_slug)
    log.info("=== Pipeline start: %s ===", slug)

    # When called from --book, find the matching spreadsheet row by slug/city
    if row_index == 0:
        row_index = find_row_for_slug(args.spreadsheet, slug)
        log.info("Matched spreadsheet row: %d", row_index)

    book = load_book_record(args.spreadsheet, row_index)
    log.info("Book loaded: %s", book.title)

    storyboard = generate_storyboard(book, slug, cache_dir=STORYBOARD_CACHE_DIR)
    log.info("Storyboard ready — city=%s, pages=%d", storyboard.city, len(storyboard.pages))

    pages_dir = PAGES_ROOT / slug
    covers_dir = COVERS_ROOT / slug
    pages_dir.mkdir(parents=True, exist_ok=True)
    covers_dir.mkdir(parents=True, exist_ok=True)

    skip_cover = getattr(args, "skip_cover", False)
    if not args.skip_images:
        provider = get_provider(args.provider)
        log.info("Image provider: %s", provider.name)

        if not skip_cover:
            cover_path = covers_dir / f"{slug}_cover.png"
            log.info("Generating cover...")
            _generate_with_retry(provider, storyboard.cover_prompt, cover_path)
        else:
            log.info("Skipping cover generation (--skip-cover set).")

        workers = getattr(args, "workers", 1)
        _generate_pages_parallel(provider, storyboard, pages_dir, slug, workers)

    image_paths = find_png_pages(pages_dir)
    interior_path = build_interior_pdf(
        book=book,
        image_paths=image_paths,
        output_dir=OUTPUT_INTERIORS,
        page_width=PAGE_WIDTH,
        page_height=PAGE_HEIGHT,
        image_margin=IMAGE_MARGIN,
    )
    log.info("Interior PDF: %s", interior_path)

    cover_image = covers_dir / f"{slug}_cover.png"
    cover_pdf_path = build_cover_pdf(
        book=book,
        cover_image_path=cover_image if cover_image.exists() else None,
        output_dir=OUTPUT_COVERS,
        city=storyboard.city,
        page_width=PAGE_WIDTH,
        page_height=PAGE_HEIGHT,
    )
    log.info("Cover PDF: %s", cover_pdf_path)

    metadata = generate_metadata(book, storyboard.city, page_count=len(image_paths))
    metadata_path = save_metadata(metadata, OUTPUT_METADATA, slug)
    log.info("Metadata: %s", metadata_path)

    from kdp_assembler import assemble_kdp_pdf
    kdp_dir = OUTPUT_KDP_READY / slug
    kdp_path = assemble_kdp_pdf(
        book=book,
        cover_image_path=cover_image,
        pages_dir=pages_dir,
        output_dir=kdp_dir,
        page_width=PAGE_WIDTH,
        page_height=PAGE_HEIGHT,
        image_margin=IMAGE_MARGIN,
        city_name=storyboard.city,
    )
    log.info("KDP-ready PDF: %s", kdp_path)

    log.info("=== Pipeline complete: %s ===", slug)
    print(f"\nDone: {slug}")
    print(f"  Interior PDF : {interior_path}")
    print(f"  Cover PDF    : {cover_pdf_path}")
    print(f"  KDP-Ready PDF: {kdp_path}")
    print(f"  Metadata     : {metadata_path}")


def run_pipeline_for_all_books(args: argparse.Namespace) -> None:
    log = logging.getLogger(__name__)

    df = pd.read_excel(args.spreadsheet, engine="openpyxl")
    if df.empty:
        log.error("Spreadsheet is empty — nothing to process.")
        return

    log.info("Running pipeline for %d books...", len(df))

    for index, row in df.iterrows():
        slug_raw = (
            row.get("book_slug") or row.get("slug")
            or row.get("city") or row.get("City")
            or row.get("book_title") or row.get("Book Title")
            or f"book_{index + 1}"
        )
        slug = slugify(str(slug_raw))

        try:
            run_pipeline_for_book(slug, args, row_index=int(index))
        except Exception as exc:
            log.error("Pipeline failed for %s: %s", slug, exc, exc_info=True)


def _generate_pages_parallel(provider, storyboard, pages_dir: Path, slug: str, workers: int) -> None:
    """Generate all interior pages, skipping those that already exist."""
    import concurrent.futures

    log = logging.getLogger(__name__)

    pending = [
        (page, pages_dir / f"{slug}_page_{page.page_number:02d}.png")
        for page in storyboard.pages
        if not (pages_dir / f"{slug}_page_{page.page_number:02d}.png").exists()
    ]

    if not pending:
        log.info("All pages already exist, skipping generation.")
        return

    def _do(args):
        page, path = args
        log.info("Generating page %02d/%d: %s", page.page_number, PAGES_PER_BOOK, page.scene_category)
        _generate_with_retry(provider, page.image_prompt, path)
        return page.page_number

    # Serial fallback when workers=1 to avoid thread overhead for API-rate-limited providers
    if workers <= 1:
        for item in pending:
            _do(item)
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_do, item): item[0].page_number for item in pending}
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                page_num = futures[future]
                log.error("Page %02d failed: %s", page_num, exc)


def _generate_with_retry(provider, prompt: str, output_path: Path, max_retries: int = 3) -> None:
    import time

    log = logging.getLogger(__name__)
    for attempt in range(1, max_retries + 1):
        try:
            provider.generate(prompt, output_path)
            return
        except Exception as exc:
            log.warning("Attempt %d/%d failed for %s: %s", attempt, max_retries, output_path.name, exc)
            if attempt < max_retries:
                time.sleep(2 ** attempt)
            else:
                raise


# ── Legacy / utility commands ──────────────────────────────────────────────────

def rename_downloaded_pages(args: argparse.Namespace) -> None:
    book_slug = slugify(args.rename)
    source_dir = args.raw_dir or RAW_DOWNLOADS_ROOT / book_slug
    destination_dir = PAGES_ROOT / book_slug

    result = rename_png_pages(
        source_dir=source_dir,
        destination_dir=destination_dir,
        book_slug=book_slug,
        copy_files=args.copy,
        overwrite=args.overwrite,
    )

    action = "Copied" if result.copied else "Moved"
    print(f"{action} {len(result.files)} PNG files")
    print(f"From: {result.source_dir}")
    print(f"To:   {result.destination_dir}")
    if result.files:
        print(f"First: {result.files[0].name}")
        print(f"Last:  {result.files[-1].name}")


def generate_interior_pdf() -> None:
    book = load_book_record(CONFIG.spreadsheet_path, CONFIG.row_index)
    image_paths = find_png_pages(CONFIG.pages_dir)
    output_path = build_interior_pdf(
        book=book,
        image_paths=image_paths,
        output_dir=CONFIG.output_dir,
        page_width=CONFIG.page_width,
        page_height=CONFIG.page_height,
        image_margin=CONFIG.image_margin,
    )
    print(f"Generated {output_path}")
    print(f"Included {len(image_paths)} coloring pages from {CONFIG.pages_dir}")


def refresh_spreadsheet_prompts(args: argparse.Namespace) -> None:
    output_path = refresh_prompt_columns(args.spreadsheet, args.output_spreadsheet)
    print(f"Refreshed prompt columns → {output_path}")


if __name__ == "__main__":
    main()
