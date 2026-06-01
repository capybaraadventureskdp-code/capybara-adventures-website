"""Generate KDP-ready metadata for one Capybara World Travel coloring book."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from book_loader import BookRecord


@dataclass
class KDPMetadata:
    title: str
    subtitle: str
    author: str
    description: str
    keywords: list[str]
    backend_keywords: str
    category: str
    page_count: int
    language: str = "English"
    book_type: str = "Paperback"


def generate_metadata(book: BookRecord, city: str, page_count: int = 30) -> KDPMetadata:
    title = f"Capybara World Travel: Coloring Book — {city}"
    subtitle = (
        f"30 Relaxing Coloring Pages for Adults and Kids | "
        f"Kawaii Capybara Adventures in {city}"
    )

    keywords = [
        f"{city.lower()} coloring book",
        "capybara coloring book",
        "kawaii coloring book adults",
        "travel coloring book kids",
        "cute animal coloring pages",
        "stress relief coloring book",
        "cozy coloring book series",
    ]

    description = (
        f"Escape into the cozy world of Capybara World Travel with this "
        f"charming {city} coloring book!\n\n"
        f"Join our adorable capybara mascot on a warm adventure through {city}, "
        "exploring iconic landmarks, tasting local flavors, meeting new friends, "
        "and collecting beautiful memories — one coloring page at a time.\n\n"
        "INSIDE THIS BOOK:\n"
        "• 30 unique story-driven coloring pages\n"
        "• Thick clean outlines and large open coloring spaces\n"
        "• Kawaii cute aesthetic — relaxing and fun to color\n"
        "• A complete journey from arrival to farewell\n"
        "• Varied compositions, poses, and scenes on every page\n"
        "• Professional quality — no grayscale fills or muddy art\n\n"
        "PERFECT FOR:\n"
        "• Adults who love stress-relief coloring\n"
        "• Kids who love cute animal characters\n"
        "• Travel lovers and thoughtful gift-givers\n"
        "• Capybara and kawaii art fans\n\n"
        f"Collect the entire Capybara World Travel series and visit the world "
        "one coloring page at a time!"
    )

    return KDPMetadata(
        title=title,
        subtitle=subtitle,
        author=book.author,
        description=description,
        keywords=keywords,
        backend_keywords=", ".join(keywords),
        category="Arts & Photography > Drawing > Coloring Books",
        page_count=page_count + 2,  # +2 for title and copyright pages
    )


def save_metadata(metadata: KDPMetadata, output_dir: Path, book_slug: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{book_slug}_metadata.json"

    data = {
        "title": metadata.title,
        "subtitle": metadata.subtitle,
        "author": metadata.author,
        "description": metadata.description,
        "keywords": metadata.keywords,
        "backend_keywords": metadata.backend_keywords,
        "category": metadata.category,
        "page_count": metadata.page_count,
        "language": metadata.language,
        "book_type": metadata.book_type,
    }

    output_path.write_text(json.dumps(data, indent=2))
    return output_path
