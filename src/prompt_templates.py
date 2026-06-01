"""Reusable prompt templates and style rules for Capybara World Travel coloring books."""

from dataclasses import dataclass
from typing import Any


# ── Brand constants ────────────────────────────────────────────────────────────

BRAND_NAME = "Capybara World Travel"

CAPYBARA_CHARACTER = (
    "cute round chubby capybara mascot, always happy, cozy, and emotionally warm, "
    "small rounded ears, friendly wholesome expression, consistent character design across all pages"
)

CHARACTER_RULES = (
    "No humans. Only anthropomorphic animals. "
    "Main character is always the capybara mascot. "
    "Other characters may be cute supporting animals when natural for the scene."
)

# ── Interior style ─────────────────────────────────────────────────────────────

INTERIOR_LINE_ART_STYLE = (
    "printable black-and-white coloring book line art, thick clean bold outlines, "
    "white background, no grayscale shading, no crosshatching, no fills, "
    "large open coloring spaces, minimal clutter, simple cozy compositions, "
    "handcrafted kawaii storybook aesthetic"
)

GLOBAL_VISUAL_RULES = (
    "make each page visually distinct from surrounding pages, "
    "vary the composition angle, capybara pose, foreground/background structure, "
    "prop, and scene scale, avoid repeating the same layout or empty-street arrangement, "
    "avoid heavy black-filled areas, no fake AI text or signs"
)

ENDING_RULE = (
    "final page must be a farewell, favourite-memory, souvenir, or recap scene — "
    "never a blank notes page"
)

# ── Cover style ────────────────────────────────────────────────────────────────

COVER_STYLE = (
    "pastel color palette, soft cheerful warm colors, gentle contrast, "
    "polished professional Amazon KDP cover design, cozy collectible series aesthetic, "
    "handcrafted storybook feel"
)

# ── Variation pools used by the spreadsheet refresh tool ──────────────────────

COMPOSITION_TYPES = [
    "left-led composition with activity on the right",
    "right-led composition with activity on the left",
    "centered character with symmetric landmark background",
    "foreground capybara with wide scenic background",
    "wide panoramic composition with small capybara in frame",
    "diagonal movement through the scene from bottom-left to top-right",
]

VISUAL_VARIATION_NOTES = [
    "change viewpoint, props, and scale compared to nearby pages",
    "use a fresh landmark, food item, vehicle, or cultural detail as the page anchor",
    "alternate close-up, medium, and wide scene framing across the book",
    "avoid repeating the same capybara placement or identical empty-street layout",
    "include a clear story action rather than a static pose",
]

ENDING_SCENE_TYPES = [
    "farewell wave scene at the departure gate",
    "favourite memory recap scene with keepsakes spread out",
    "souvenir celebration scene with local items",
    "group photo recap scene with new animal friends",
    "map-and-memories closing scene with postcards",
]


@dataclass(frozen=True)
class PromptFields:
    """Generated prompt and planning fields for one spreadsheet row."""

    interior_prompt: str
    cover_prompt: str
    color_style: str
    story_notes: str
    composition_type: str
    visual_variation_notes: str
    ending_scene_type: str


def build_prompt_fields(row: dict[str, Any], row_number: int) -> PromptFields:
    """Build capybara-branded prompt fields for a spreadsheet row."""

    title = _text(row, "book_title", f"{BRAND_NAME}: Coloring Book")
    theme = _text(row, "theme", "world travel adventure")
    city = _text(row, "city", _text(row, "City", "an exciting destination"))
    landmarks = _text(row, "landmarks", "")
    cultural_elements = _text(row, "cultural_elements", "")
    nature_elements = _text(row, "nature_elements", "")
    cover_direction = _text(row, "cover_direction", "")

    composition_type = _pick(COMPOSITION_TYPES, row_number)
    visual_variation_notes = _pick(VISUAL_VARIATION_NOTES, row_number)
    ending_scene_type = _pick(ENDING_SCENE_TYPES, row_number)

    subject_details = _join_present(
        [
            f"theme: {theme}",
            f"city/destination: {city}",
            f"landmarks: {landmarks}" if landmarks else "",
            f"cultural details: {cultural_elements}" if cultural_elements else "",
            f"nature details: {nature_elements}" if nature_elements else "",
        ]
    )

    interior_prompt = (
        f"Coloring book interior page for '{title}'. "
        f"Character: {CAPYBARA_CHARACTER}. "
        f"Style: {INTERIOR_LINE_ART_STYLE}. "
        f"Composition: {composition_type}. "
        f"{GLOBAL_VISUAL_RULES}. {visual_variation_notes}. "
        f"{subject_details}. "
        f"{CHARACTER_RULES} "
        "Clear focal point, strong storytelling action, relaxing balanced layout."
    )

    cover_direction_text = cover_direction or f"iconic {city} landmarks and cultural symbols"
    cover_prompt = (
        f"Premium full-color Amazon KDP cover for '{title}'. "
        f"Brand: {BRAND_NAME}. "
        f"{COVER_STYLE}. "
        f"Central illustration: {CAPYBARA_CHARACTER}, holding a small {city} souvenir, "
        f"surrounded by {cover_direction_text}. "
        "Visually striking thumbnail, large readable title area, "
        "no dark heavy fills, no cluttered text zones."
    )

    story_notes = (
        "Follow a clear beginning-middle-ending journey arc. "
        "Vary compositions, capybara placement, scene scale, props, and viewpoints so pages feel fresh. "
        "Keep interiors open and colorable with large white spaces; avoid heavy black-filled scenes. "
        f"Ending rule: {ENDING_RULE}. Suggested ending type: {ending_scene_type}."
    )

    return PromptFields(
        interior_prompt=interior_prompt,
        cover_prompt=cover_prompt,
        color_style="pastel-inspired cover palette; black-and-white open-space interiors",
        story_notes=story_notes,
        composition_type=composition_type,
        visual_variation_notes=visual_variation_notes,
        ending_scene_type=ending_scene_type,
    )


# ── Helpers ────────────────────────────────────────────────────────────────────

def _pick(options: list[str], row_number: int) -> str:
    return options[(row_number - 1) % len(options)]


def _text(row: dict[str, Any], key: str, default: str) -> str:
    value = row.get(key, default)
    if value is None:
        return default
    text = str(value).strip()
    return text if text and text.lower() != "nan" else default


def _join_present(parts: list[str]) -> str:
    return "; ".join(part for part in parts if part)
