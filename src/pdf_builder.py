"""Build the KDP interior PDF with ReportLab."""

from datetime import date
from pathlib import Path
import re

from reportlab.lib.colors import black, white
from reportlab.lib.pagesizes import portrait
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from book_loader import BookRecord
from image_utils import fit_size, load_on_white


def build_interior_pdf(
    book: BookRecord,
    image_paths: list[Path],
    output_dir: Path,
    page_width: float,
    page_height: float,
    image_margin: float,
) -> Path:
    """Create a title page, copyright page, and one page per PNG."""

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{_slugify(book.title)}_interior.pdf"

    pdf = canvas.Canvas(str(output_path), pagesize=portrait((page_width, page_height)))
    _draw_title_page(pdf, book, page_width, page_height)
    _draw_copyright_page(pdf, book, page_width, page_height)

    for image_path in image_paths:
        _draw_image_page(pdf, image_path, page_width, page_height, image_margin)
        _draw_bleedthrough_page(pdf, page_width, page_height)

    pdf.save()
    return output_path


def _draw_title_page(pdf: canvas.Canvas, book: BookRecord, page_width: float, page_height: float) -> None:
    _paint_white_page(pdf, page_width, page_height)
    pdf.setFillColor(black)

    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(page_width / 2, page_height * 0.58, book.title)

    if book.subtitle:
        pdf.setFont("Helvetica", 16)
        pdf.drawCentredString(page_width / 2, page_height * 0.52, book.subtitle)

    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(page_width / 2, page_height * 0.40, f"By {book.author}")
    pdf.showPage()


def _draw_copyright_page(pdf: canvas.Canvas, book: BookRecord, page_width: float, page_height: float) -> None:
    _paint_white_page(pdf, page_width, page_height)
    left = 1.0 * 72
    top = page_height - 1.5 * 72
    year = date.today().year

    pdf.setFillColor(black)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(left, top, "Copyright")

    pdf.setFont("Helvetica", 11)
    lines = [
        f"Copyright (c) {year} {book.copyright_name}. All rights reserved.",
        "",
        "No part of this book may be reproduced or transmitted in any form without written permission,",
        "except for brief quotations used in reviews.",
        "",
        "Printed for personal coloring and creative use.",
    ]
    y = top - 30
    for line in lines:
        pdf.drawString(left, y, line)
        y -= 16
    pdf.showPage()


def _draw_image_page(
    pdf: canvas.Canvas,
    image_path: Path,
    page_width: float,
    page_height: float,
    image_margin: float,
) -> None:
    _paint_white_page(pdf, page_width, page_height)

    image = load_on_white(image_path)
    max_width = page_width - (2 * image_margin)
    max_height = page_height - (2 * image_margin)
    draw_width, draw_height = fit_size(image.width, image.height, max_width, max_height)
    x = (page_width - draw_width) / 2
    y = (page_height - draw_height) / 2

    pdf.drawImage(ImageReader(image), x, y, width=draw_width, height=draw_height)
    pdf.showPage()


def _draw_bleedthrough_page(pdf: canvas.Canvas, page_width: float, page_height: float) -> None:
    _paint_white_page(pdf, page_width, page_height)
    pdf.setFillColor(black)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        page_width / 2,
        page_height / 2,
        "This page is intentionally left blank to prevent color bleed-through.",
    )
    pdf.showPage()


def _paint_white_page(pdf: canvas.Canvas, page_width: float, page_height: float) -> None:
    pdf.setFillColor(white)
    pdf.rect(0, 0, page_width, page_height, fill=1, stroke=0)


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return slug or "coloring_book"
