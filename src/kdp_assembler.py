"""Assemble the final KDP-ready PDF: cover + front matter + coloring pages.

PDF layout:
  Page 1  — Full-bleed cover image (AI-generated with title text embedded)
  Page 2  — Title page  (Capybara Adventures / [City] / Coloring Books / tagline)
  Page 3  — Copyright page
  Page 4  — Series page (Collect all the adventures!)
  Page 5  — Coloring page 1
  Page 6  — Blank bleed-through
  ...
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import black, white, HexColor
from reportlab.lib.pagesizes import portrait
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from book_loader import BookRecord
from image_utils import find_png_pages, fit_size

# Update this list as new books are published
_SERIES_TITLES = [
    "New York City",
    "Tokyo",
    "Venice",
    "Iceland",
    "Mexico City",
    "Egypt",
]

_ACCENT = HexColor("#C0392B")   # warm red for city name on title page


def assemble_kdp_pdf(
    book: BookRecord,
    cover_image_path: Path,
    pages_dir: Path,
    output_dir: Path,
    page_width: float,
    page_height: float,
    image_margin: float,
    city_name: str = "",
    omit_page_numbers: set | None = None,
) -> Path:
    """Build the single combined PDF ready for KDP upload."""

    output_dir.mkdir(parents=True, exist_ok=True)
    # Use city_name for slug if provided (for correct filename when spreadsheet title mismatches)
    slug = _slugify(f"Explore {city_name}") if city_name else _slugify(book.title)
    output_path = output_dir / f"{slug}_KDP_READY.pdf"

    all_image_paths = find_png_pages(pages_dir)
    if omit_page_numbers:
        image_paths = [
            p for p in all_image_paths
            if int(p.stem.split("_page_")[1]) not in omit_page_numbers
        ]
    else:
        image_paths = all_image_paths

    city = city_name or _extract_city(book)

    pdf = canvas.Canvas(str(output_path), pagesize=portrait((page_width, page_height)))

    # ── Page 1: Full-bleed cover ───────────────────────────────────────────────
    if cover_image_path and cover_image_path.exists():
        from PIL import Image as PILImage
        img = PILImage.open(str(cover_image_path)).convert("RGB")
        pdf.drawImage(ImageReader(img), 0, 0, width=page_width, height=page_height,
                      preserveAspectRatio=False)
    else:
        _white_page(pdf, page_width, page_height)
        _ctext(pdf, "Capybara Adventures", page_width, page_height * 0.60, 32, bold=True)
        _ctext(pdf, city, page_width, page_height * 0.52, 42, bold=True)
        _ctext(pdf, "Coloring Books", page_width, page_height * 0.44, 20)
    pdf.showPage()

    # ── Page 2: Title page ─────────────────────────────────────────────────────
    _white_page(pdf, page_width, page_height)
    mid = page_height / 2
    pdf.setFillColor(black)
    _ctext(pdf, "Capybara Adventures", page_width, mid + 90, 34, bold=True)
    pdf.setFillColor(_ACCENT)
    _ctext(pdf, city, page_width, mid + 18, 52, bold=True)
    pdf.setFillColor(black)
    _ctext(pdf, "Coloring Books", page_width, mid - 46, 22)
    _ctext(pdf, "For little explorers everywhere.", page_width, mid - 84, 13, italic=True)
    pdf.showPage()

    # ── Page 3: Copyright page ─────────────────────────────────────────────────
    _white_page(pdf, page_width, page_height)
    mid = page_height / 2
    pdf.setFillColor(black)
    entries = [
        ("Copyright © 2026", 14, False),
        ("", 8, False),
        ("Capybara Adventures Publishing", 14, True),
        ("", 8, False),
        ("All rights reserved.", 11, False),
        ("", 6, False),
        ("Created for personal coloring enjoyment.", 11, False),
        ("", 16, False),
        ("Visit us:", 11, False),
        ("capybaraadventures.com", 12, True),
        ("", 16, False),
        ("For All Ages", 12, False),
    ]
    # Calculate total block height and start from center
    total_h = sum(size + (6 if text else 0) for text, size, _ in entries)
    y = mid + total_h / 2
    for text, size, bold in entries:
        if not text:
            y -= size
            continue
        _ctext(pdf, text, page_width, y, size, bold=bold)
        y -= size + 6
    pdf.showPage()

    # ── Page 4: Series page ────────────────────────────────────────────────────
    _white_page(pdf, page_width, page_height)
    mid = page_height / 2
    pdf.setFillColor(black)
    _ctext(pdf, "Collect all the adventures!", page_width, mid + 130, 22, bold=True)
    y = mid + 82
    _ctext(pdf, "Capybara Adventures:", page_width, y, 13)
    y -= 30
    for title in _SERIES_TITLES:
        _ctext(pdf, title, page_width, y, 16, bold=True)
        y -= 26
    y -= 12
    _ctext(pdf, "More adventures coming soon!", page_width, y, 12, italic=True)
    pdf.showPage()

    # ── Pages 5+: Coloring pages + blank bleed-through ─────────────────────────
    for image_path in image_paths:
        from PIL import Image as PILImage
        _white_page(pdf, page_width, page_height)
        img = PILImage.open(str(image_path)).convert("RGB")
        max_w = page_width - 2 * image_margin
        max_h = page_height - 2 * image_margin
        draw_w, draw_h = fit_size(img.width, img.height, max_w, max_h)
        x = (page_width - draw_w) / 2
        y = (page_height - draw_h) / 2
        pdf.drawImage(ImageReader(img), x, y, width=draw_w, height=draw_h)
        pdf.showPage()

        _white_page(pdf, page_width, page_height)
        pdf.setFillColor(black)
        pdf.setFont("Helvetica", 9)
        pdf.drawCentredString(
            page_width / 2, page_height / 2,
            "This page is intentionally left blank to prevent color bleed-through.",
        )
        pdf.showPage()

    pdf.save()
    return output_path


# ── Helpers ────────────────────────────────────────────────────────────────────

def _ctext(
    pdf: canvas.Canvas, text: str, page_width: float, y: float, size: float,
    bold: bool = False, italic: bool = False,
) -> None:
    if bold and italic:
        font = "Helvetica-BoldOblique"
    elif bold:
        font = "Helvetica-Bold"
    elif italic:
        font = "Helvetica-Oblique"
    else:
        font = "Helvetica"
    pdf.setFont(font, size)
    pdf.drawCentredString(page_width / 2, y, text)


def _white_page(pdf: canvas.Canvas, w: float, h: float) -> None:
    pdf.setFillColor(white)
    pdf.rect(0, 0, w, h, fill=1, stroke=0)


def _extract_city(book: BookRecord) -> str:
    for key in ("city", "City", "theme", "Theme"):
        val = book.raw.get(key, "")
        if val and str(val).strip() and str(val).strip().lower() != "nan":
            return str(val).strip().title()
    if "—" in book.title:
        return book.title.split("—")[-1].strip()
    return book.title.strip()


def _slugify(value: str) -> str:
    import re
    return re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_") or "coloring_book"
