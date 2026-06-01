"""Project-wide configuration for the KDP coloring book pipeline."""

import os
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib.units import inch


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# ── Asset storage ──────────────────────────────────────────────────────────────
ASSETS_ROOT = PROJECT_ROOT / "assets"
PAGES_ROOT = ASSETS_ROOT / "pages"
COVERS_ROOT = ASSETS_ROOT / "covers"
RAW_DOWNLOADS_ROOT = ASSETS_ROOT / "raw_downloads"

# ── Pipeline outputs ───────────────────────────────────────────────────────────
OUTPUT_ROOT = PROJECT_ROOT / "output"
OUTPUT_INTERIORS = OUTPUT_ROOT / "interiors"
OUTPUT_COVERS = OUTPUT_ROOT / "covers"
OUTPUT_METADATA = OUTPUT_ROOT / "metadata"
OUTPUT_KDP_READY = OUTPUT_ROOT / "kdp_ready"
STORYBOARD_CACHE_DIR = OUTPUT_ROOT / "storyboards"

# ── Logs ───────────────────────────────────────────────────────────────────────
LOGS_ROOT = PROJECT_ROOT / "logs"

# ── Data / spreadsheets ────────────────────────────────────────────────────────
DATA_ROOT = PROJECT_ROOT / "data"
SPREADSHEET_PATH = DATA_ROOT / "kdp_coloring_book_automation_ready.xlsx"

# ── Reference materials (examples + prompt PDF) ────────────────────────────────
EXAMPLES_ROOT = PROJECT_ROOT / "Capybara_Coloring_Books"
COLORING_EXAMPLES_DIR = EXAMPLES_ROOT / "Coloring_sheet_examples"
COVER_EXAMPLES_DIR = EXAMPLES_ROOT / "Cover_page_examples"
PROMPT_PDF = EXAMPLES_ROOT / "Coloring book prompt.pdf"

# ── KDP page dimensions ────────────────────────────────────────────────────────
PAGE_WIDTH = 8.5 * inch
PAGE_HEIGHT = 11.0 * inch
IMAGE_MARGIN = 0.5 * inch
PAGES_PER_BOOK = 30

# ── Image generation ───────────────────────────────────────────────────────────
# Override with the IMAGE_PROVIDER env var or the --provider CLI flag.
# Options: "stub" (no API key needed) | "gemini" (requires GOOGLE_API_KEY)
DEFAULT_IMAGE_PROVIDER: str = os.environ.get("IMAGE_PROVIDER", "stub")


# ── Legacy dataclass — kept for backward compatibility with older scripts ──────

@dataclass(frozen=True)
class InteriorConfig:
    """Static layout and path settings for the interior PDF."""

    spreadsheet_path: Path = SPREADSHEET_PATH
    pages_dir: Path = PAGES_ROOT / "explore_tokyo"
    output_dir: Path = OUTPUT_INTERIORS
    page_width: float = PAGE_WIDTH
    page_height: float = PAGE_HEIGHT
    image_margin: float = IMAGE_MARGIN
    row_index: int = 0


CONFIG = InteriorConfig()
