"""Image discovery and preparation helpers."""

from pathlib import Path
import re

from PIL import Image


def find_png_pages(pages_dir: Path) -> list[Path]:
    """Return PNG page assets in natural filename order."""

    pages = sorted(pages_dir.glob("*.png"), key=_natural_key)
    if not pages:
        raise FileNotFoundError(f"No PNG files found in {pages_dir}")
    return pages


def load_on_white(image_path: Path) -> Image.Image:
    """Open a PNG and flatten any transparency onto a white RGB background."""

    source = Image.open(image_path).convert("RGBA")
    white = Image.new("RGBA", source.size, "WHITE")
    white.alpha_composite(source)
    return white.convert("RGB")


def fit_size(width: float, height: float, max_width: float, max_height: float) -> tuple[float, float]:
    """Scale dimensions to fit inside a box while preserving aspect ratio."""

    scale = min(max_width / width, max_height / height)
    return width * scale, height * scale


def _natural_key(path: Path) -> list[int | str]:
    parts = re.split(r"(\d+)", path.name)
    return [int(part) if part.isdigit() else part.lower() for part in parts]
