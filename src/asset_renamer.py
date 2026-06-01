"""Rename raw downloaded PNGs into clean sequential coloring page assets."""

from dataclasses import dataclass
from pathlib import Path
import re
import shutil
from uuid import uuid4


@dataclass(frozen=True)
class RenameResult:
    """Summary of a completed page asset rename operation."""

    source_dir: Path
    destination_dir: Path
    files: list[Path]
    copied: bool


def rename_png_pages(
    source_dir: Path,
    destination_dir: Path,
    book_slug: str,
    *,
    copy_files: bool = False,
    overwrite: bool = False,
) -> RenameResult:
    """Move or copy PNGs from a raw folder into sequential page names."""

    clean_slug = slugify(book_slug)
    source_dir = source_dir.expanduser().resolve()
    destination_dir = destination_dir.expanduser().resolve()

    if not source_dir.exists():
        raise FileNotFoundError(f"Raw download folder does not exist: {source_dir}")
    if not source_dir.is_dir():
        raise NotADirectoryError(f"Raw download path is not a folder: {source_dir}")

    png_files = find_raw_pngs(source_dir)
    if not png_files:
        raise FileNotFoundError(f"No PNG files found in raw download folder: {source_dir}")

    destination_dir.mkdir(parents=True, exist_ok=True)
    planned_files = [
        destination_dir / f"{clean_slug}_page_{index:02d}.png"
        for index, _ in enumerate(png_files, start=1)
    ]
    _guard_existing_files(planned_files, overwrite)

    if copy_files:
        for source, target in zip(png_files, planned_files):
            shutil.copy2(source, target)
    else:
        _move_files_safely(png_files, planned_files)

    return RenameResult(
        source_dir=source_dir,
        destination_dir=destination_dir,
        files=planned_files,
        copied=copy_files,
    )


def find_raw_pngs(source_dir: Path) -> list[Path]:
    """Return raw PNGs in deterministic natural-name order, ignoring other files."""

    png_files = [
        path
        for path in source_dir.iterdir()
        if path.is_file() and path.suffix.lower() == ".png"
    ]
    return sorted(png_files, key=_natural_key)


def slugify(value: str) -> str:
    """Normalize a user-provided book slug for filenames and folders."""

    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    if not slug:
        raise ValueError("Book slug cannot be empty")
    return slug


def _guard_existing_files(planned_files: list[Path], overwrite: bool) -> None:
    if overwrite:
        return

    existing = [path for path in planned_files if path.exists()]
    if existing:
        names = ", ".join(path.name for path in existing[:5])
        extra = "" if len(existing) <= 5 else f", and {len(existing) - 5} more"
        raise FileExistsError(
            f"Destination file already exists: {names}{extra}. "
            "Use --overwrite to replace existing pages."
        )


def _move_files_safely(source_files: list[Path], target_files: list[Path]) -> None:
    """Move files through temporary names so same-folder renames cannot collide."""

    temporary_files: list[Path] = []
    for source in source_files:
        temporary = source.with_name(f".renaming_{uuid4().hex}_{source.name}")
        shutil.move(source, temporary)
        temporary_files.append(temporary)

    for temporary, target in zip(temporary_files, target_files):
        if target.exists():
            target.unlink()
        shutil.move(temporary, target)


def _natural_key(path: Path) -> list[int | str]:
    parts = re.split(r"(\d+)", path.name)
    return [int(part) if part.isdigit() else part.lower() for part in parts]
