"""Load one coloring book metadata row from the planning spreadsheet."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class BookRecord:
    """Small normalized view of the spreadsheet fields the PDF needs."""

    title: str
    subtitle: str
    author: str
    copyright_name: str
    raw: dict[str, Any]


def load_book_record(spreadsheet_path: Path, row_index: int = 0) -> BookRecord:
    """Read one row from the Excel workbook and normalize likely metadata fields."""

    df = pd.read_excel(spreadsheet_path, engine="openpyxl")
    if df.empty:
        raise ValueError(f"No rows found in {spreadsheet_path}")
    if row_index < 0 or row_index >= len(df):
        raise IndexError(f"Row index {row_index} is outside spreadsheet range 0..{len(df) - 1}")

    row = df.iloc[row_index].dropna().to_dict()
    return BookRecord(
        title=_first_present(
            row,
            [
                "title",
                "book_title",
                "Book Title",
                "Title",
                "kdp_title",
                "KDP Title",
            ],
            default="Explore Tokyo Coloring Book",
        ),
        subtitle=_first_present(
            row,
            ["subtitle", "book_subtitle", "Book Subtitle", "Subtitle", "kdp_subtitle"],
            default="A Coloring Adventure",
        ),
        author=_first_present(
            row,
            ["author", "Author", "pen_name", "Pen Name", "brand", "Brand"],
            default="Independent Publishing",
        ),
        copyright_name=_first_present(
            row,
            ["copyright", "Copyright", "copyright_name", "Copyright Name", "author", "Author"],
            default="Independent Publishing",
        ),
        raw=row,
    )


def find_row_for_slug(spreadsheet_path: Path, slug: str) -> int:
    """Return the first row index whose city/title/slug matches slug (case-insensitive).

    Falls back to row 0 if no match is found.
    """
    import re

    def _slugify(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")

    target = _slugify(slug)
    df = pd.read_excel(spreadsheet_path, engine="openpyxl")

    search_columns = ["book_slug", "slug", "city", "City", "book_title", "Book Title"]
    for col in search_columns:
        if col not in df.columns:
            continue
        for idx, value in df[col].items():
            if pd.isna(value):
                continue
            if _slugify(str(value)) == target:
                return int(idx)

    return 0


def _first_present(row: dict[str, Any], names: list[str], default: str) -> str:
    for name in names:
        value = row.get(name)
        if value is not None and str(value).strip():
            return str(value).strip()
    return default
