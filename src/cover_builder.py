"""Build the KDP cover PDF for one Capybara World Travel book."""

from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib.colors import black, HexColor
from reportlab.lib.pagesizes import portrait
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from book_loader import BookRecord
from image_utils import fit_size, load_on_white


_BG_COLOR = HexColor("#FFF8F0")   # warm off-white matching the brand palette


def build_cover_pdf(
    book: BookRecord,
    cover_image_path: Path | None,
    output_dir: Path,
    city: str,
    page_width: float,
    page_height: float,
) -> Path:
    """Create a KDP cover PDF. Falls back to a type-only cover if no image is provided."""

    output_dir.mkdir(parents=True, exist_ok=True)
    slug = _slugify(city)
    output_path = output_dir / f"{slug}_cover.pdf"

    pdf = canvas.Canvas(str(output_path), pagesize=portrait((page_width, page_height)))

    if cover_image_path and cover_image_path.exists():
        _draw_illustrated_cover(pdf, book, cover_image_path, city, page_width, page_height)
    else:
        _draw_text_cover(pdf, book, city, page_width, page_height)

    pdf.save()
    return output_path


def _draw_illustrated_cover(
    pdf: canvas.Canvas,
    book: BookRecord,
    cover_image_path: Path,
    city: str,
    page_width: float,
    page_height: float,
) -> None:
    # Full bleed — the AI-generated image already contains the title text.
    # Stretch to fill the entire page with no margins and no overlaid text.
    from PIL import Image as PILImage
    img = PILImage.open(str(cover_image_path)).convert("RGB")
    pdf.drawImage(ImageReader(img), 0, 0, width=page_width, height=page_height,
                  preserveAspectRatio=False)
    pdf.showPage()


def _draw_text_cover(
    pdf: canvas.Canvas,
    book: BookRecord,
    city: str,
    page_width: float,
    page_height: float,
) -> None:
    _fill_bg(pdf, page_width, page_height)

    mid = page_height / 2
    pdf.setFillColor(black)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(page_width / 2, mid + 50, "Capybara World Travel")

    pdf.setFont("Helvetica-Bold", 34)
    pdf.drawCentredString(page_width / 2, mid, f"Coloring Book — {city}")

    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(page_width / 2, mid - 42, "30 Relaxing Coloring Pages")

    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(page_width / 2, mid - 70, f"By {book.author}")

    pdf.showPage()


def _fill_bg(pdf: canvas.Canvas, page_width: float, page_height: float) -> None:
    pdf.setFillColor(_BG_COLOR)
    pdf.rect(0, 0, page_width, page_height, fill=1, stroke=0)


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return slug or "cover"
