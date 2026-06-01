"""Generate a 30-page sequential storyboard for one Capybara World Travel coloring book."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import Any

import json

from book_loader import BookRecord
from character_bible import build_character_block, build_cover_character_block
from config import DATA_ROOT

_CITY_SCENES_DIR = DATA_ROOT / "city_scenes"

_INTERIOR_STYLE = (
    "black-and-white coloring book line art only, thick clean outlines, "
    "no shading, no grayscale, no crosshatching, no sketch texture, no dark fills, "
    "large open coloring spaces, minimal details, one clear activity per page, "
    "simple uncluttered composition, lots of white space, soft storybook feeling, "
    "cozy kawaii children's-book style, Sanrio-like emotional warmth"
)

_COVER_STYLE = (
    "full-color premium illustration, cozy kawaii aesthetic, handcrafted storybook feeling, "
    "soft pastel palette (cream, peach, dusty pink, soft sky blue, warm white, soft mint), "
    "soft daytime lighting, NOT realistic, NOT CGI, NOT glossy 3D, NOT hyper-detailed AI art, "
    "collectible indie children's-book branding, highly appealing thumbnail design"
)

_INTERIOR_RULES = (
    "No humans ever. "
    "Include 1 small cute companion animal in most scenes (bird, bunny, cat, duck, fox, panda, turtle, or deer) — "
    "companion is about 1/3 the size of Capy and wears simple destination-appropriate clothing. "
    "No fake text or readable signage inside the illustration. "
    "No crowded scenes. No complicated architecture. No tiny unreadable details. "
    "Vary Capy's pose, eye direction, and placement from nearby pages. "
    "Keep backgrounds simple and supportive — one or two landmark elements, not a full cityscape. "
    "Prioritize large open coloring spaces over environmental detail."
)

_COVER_RULES = (
    "No humans. Clear large centered title area. Strong focal capybara mascot in foreground. "
    "Destination landmarks in background. Minimal clutter. Balanced cozy composition. "
    "No fake AI-generated signage."
)


# ── Narrative arc ──────────────────────────────────────────────────────────────
# Each entry: (page_number, scene_category, scene_template, pose_hint)
# {city} and {landmark_N} are substituted at build time.
# pose_hint drives visual variety — different angle/direction each page.

_ARC: list[tuple[int, str, str, str]] = [
    (1,  "arrival",       "Capybara arrives at the {city} international airport, dragging a rolling suitcase and waving at a flight arrivals board, body facing left, looking over right shoulder toward the exit signs", "wide shot, low angle, airport terminal background with gates and windows"),
    (2,  "first_glimpse", "Capybara stands at the city edge seeing {landmark_0} for the very first time, mouth open in amazement, both arms raised wide, looking straight up", "medium shot, straight-on angle, dramatic upward gaze, landmark towers behind"),
    (3,  "hotel",         "Capybara kneels on a traditional {city} inn floor unpacking a tiny suitcase onto tatami or a cozy bed, back slightly turned, looking down with a happy expression", "close-up, top-down angle, cozy inn room details around"),
    (4,  "breakfast",     "Capybara sits at a low breakfast counter eating {food_0} with chopsticks, hunched forward excitedly, eyes wide, steam rising from the food", "medium close-up, side profile facing right, counter and morning light background"),
    (5,  "landmark_1",    "Capybara stands on tiptoe in front of {landmark_1}, one paw pointing dramatically at it, body facing right, chin tilted up proudly", "full body shot, three-quarter angle, landmark prominent behind"),
    (6,  "photo",         "Capybara holds up a tiny camera with both paws, squinting one eye to look through the viewfinder, photographing {landmark_2} behind them, body facing forward", "medium shot, straight-on, landmark framed in the background over capybara's shoulder"),
    (7,  "market",        "Capybara crouches down low examining a stall of {cultural_0} goods, one paw on chin, leaning far forward curiously, facing left", "medium shot, slight low angle, busy colorful market stalls surrounding"),
    (8,  "street_food",   "Capybara holds a skewer of {food_1} high above their head in triumph, mouth open wide with delight, body facing the viewer, other arm out for balance", "close-up, straight-on, street food stall in soft background"),
    (9,  "park",          "Capybara lies on their back in a {city} garden under {nature_0} trees, arms and legs spread wide, smiling up at the sky with eyes closed in bliss", "wide overhead-style view, peaceful garden setting, petals floating"),
    (10, "local_animal",  "Capybara kneels face-to-face with a small {city} local animal friend, both leaning toward each other nose-to-nose, surprised happy expressions", "tight two-shot, eye-level, simple natural background"),
    (11, "transport",     "Capybara leans out of a {city} train or ferry window, one arm waving wildly, scarf blowing behind, facing right with wind-blown cheeks", "medium shot, three-quarter facing right, landscape rushing past the window"),
    (12, "landmark_2",    "Capybara sits cross-legged on the ground sketching {landmark_3} in a notebook, tongue out in concentration, book propped on knees, body facing slightly left", "medium shot, side angle, landmark detailed in the distance behind"),
    (13, "shopping",      "Capybara stands in a {city} souvenir shop holding up two different trinkets, one in each paw, looking back and forth between them with a delighted confused face", "medium close-up, straight-on, shelves of colorful souvenirs packed behind"),
    (14, "craft",         "Capybara bends over a craft table learning {cultural_1} with both paws working carefully, brow furrowed in happy concentration, body turned sideways", "close-up, slight overhead, craft materials spread around the table"),
    (15, "temple",        "Capybara walks slowly through a towering {city} temple gate, one paw touching the wooden pillar, looking up at the architecture with quiet awe, body small against the large gate", "full body, low angle looking up, gate towering above filling the frame"),
    (16, "viewpoint",     "Capybara sits alone at a hilltop or roof-deck railing overlooking {city} at golden hour, chin resting on paws, gazing peacefully into the distance, profile facing right", "wide shot, side profile, sweeping city panorama stretching behind"),
    (17, "snack",         "Capybara sits wrapped in a cozy scarf at a tiny café table, holding an oversized cup of {food_2} in both paws, eyes crescent with happiness, steam rising", "cozy close-up, three-quarter facing left, warm café window light"),
    (18, "festival",      "Capybara skips gleefully through a {city} festival crowd, arms raised clapping, confetti or lanterns flying around, facing forward with a huge grin", "medium shot, dynamic energy, festival lanterns and decorations surrounding"),
    (19, "dinner",        "Capybara sits at a restaurant table with a steaming bowl of {food_3} before them, chopsticks raised mid-slurp, eyes crescent and cheeks puffed with delight", "medium close-up, straight-on, warm restaurant lantern light background"),
    (20, "evening_walk",  "Capybara strolls along a {city} riverside promenade at dusk holding a paper lantern, silhouette soft against glowing lanterns on the water, facing left", "wide shot, side profile, lantern light and water reflections behind"),
    (21, "museum",        "Capybara stands before a giant exhibit at a {city} museum — perhaps huge samurai armor or a dinosaur skeleton — body tiny compared to the exhibit, neck craned up, jaw dropped", "dramatic low angle, capybara small in foreground, exhibit towering behind"),
    (22, "outdoor",       "Capybara cycles energetically along a {city} path beside {nature_1}, legs pedaling fast, hair blowing, big grin, heading right across the page", "medium wide shot, facing right, nature scenery rushing past"),
    (23, "waterside",     "Capybara sits on the edge of a {city} dock or riverbank, feet dangling over the water, leaning back on both arms, gazing dreamily at the reflection below", "medium shot, slight overhead, water and city reflection below"),
    (24, "sport",         "Capybara tries {cultural_2} sport or activity with hilariously determined effort — arms flailing, legs wide, expression of total concentration", "action medium shot, dynamic pose, sports setting or arena around"),
    (25, "art_market",    "Capybara holds up an enormous handmade {city} craft item bigger than their own body, laughing with delight, barely visible behind it, facing viewer", "medium shot, straight-on comedy framing, market stalls around"),
    (26, "celebration",   "Capybara joins a {city} seasonal celebration, dancing in a conga line of cute animals, arms on shoulders of animal in front, all bouncing in step", "wide group shot, slight diagonal, festive decorations filling the scene"),
    (27, "new_friends",   "Capybara stands in the center of a semicircle of three adorable animal friends (bunny, bird, panda) exchanging small gifts, all smiling, capybara holding a tiny wrapped box", "medium group shot, straight-on warm composition, simple background"),
    (28, "packing",       "Capybara sits on top of an overstuffed suitcase to close it, both feet pushing down, arms spread, expression of cheerful determination, surrounded by souvenirs", "medium close-up, slight overhead angle, suitcase chaos spread around"),
    (29, "farewell",      "Capybara stands at the departure gate window pressing one paw against the glass, looking back over shoulder at the {city} skyline with teary happy eyes", "medium shot, three-quarter back angle, city skyline visible through window"),
    (30, "memories",      "Capybara sits surrounded by a spread of Polaroid photos, souvenirs, local food packaging, and keepsakes from {city}, holding up one favorite photo and smiling", "overhead wide shot, all items arranged around capybara like a scrapbook"),
]


# ── Per-page specific element assignment ───────────────────────────────────────

def _assign_elements(landmarks: str, cultural: str, nature: str) -> dict[str, str]:
    """Split landmark/cultural/nature lists and assign to named slots."""
    def _split(s: str) -> list[str]:
        return [x.strip() for x in s.split(";") if x.strip()] or [""]

    lm = _split(landmarks)
    cu = _split(cultural)
    na = _split(nature)

    # Build enough slots to cover all 30 pages by cycling
    return {
        f"landmark_{i}": lm[i % len(lm)] for i in range(10)
    } | {
        f"cultural_{i}": cu[i % len(cu)] for i in range(10)
    } | {
        f"food_{i}": cu[i % len(cu)] for i in range(10)
    } | {
        f"nature_{i}": na[i % len(na)] for i in range(10)
    }


# ── Data classes ───────────────────────────────────────────────────────────────

@dataclass
class PageConcept:
    page_number: int
    scene_category: str
    scene_description: str
    image_prompt: str


@dataclass
class Storyboard:
    book_slug: str
    city: str
    cover_prompt: str
    pages: list[PageConcept] = field(default_factory=list)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self._to_dict(), indent=2))

    @classmethod
    def load(cls, path: Path) -> "Storyboard":
        data = json.loads(path.read_text())
        pages = [
            PageConcept(
                page_number=p["page_number"],
                scene_category=p["scene_category"],
                scene_description=p["scene_description"],
                image_prompt=p["image_prompt"],
            )
            for p in data["pages"]
        ]
        return cls(
            book_slug=data["book_slug"],
            city=data["city"],
            cover_prompt=data["cover_prompt"],
            pages=pages,
        )

    def _to_dict(self) -> dict[str, Any]:
        return {
            "book_slug": self.book_slug,
            "city": self.city,
            "cover_prompt": self.cover_prompt,
            "pages": [
                {
                    "page_number": p.page_number,
                    "scene_category": p.scene_category,
                    "scene_description": p.scene_description,
                    "image_prompt": p.image_prompt,
                }
                for p in self.pages
            ],
        }


# ── Public API ─────────────────────────────────────────────────────────────────

def generate_storyboard(
    book: BookRecord,
    book_slug: str,
    cache_dir: Path | None = None,
) -> Storyboard:
    """Build a 30-page storyboard, loading from cache if it already exists."""

    if cache_dir:
        cache_path = cache_dir / f"{book_slug}_storyboard.json"
        if cache_path.exists():
            return Storyboard.load(cache_path)

    city = _extract_city(book)
    landmarks = _get_field(book, "landmarks", "")
    cultural = _get_field(book, "cultural_elements", "")
    nature = _get_field(book, "nature_elements", "")

    # If the scene file defines its own city (overrides spreadsheet row mismatch)
    scene_file = _CITY_SCENES_DIR / f"{book_slug}_scenes.json"
    if scene_file.exists():
        import json as _json
        _scene_data = _json.loads(scene_file.read_text())
        if _scene_data.get("city") and _scene_data["city"].lower() != city.lower():
            city = _scene_data["city"]
            # Use landmarks from scene file if present, otherwise keep spreadsheet ones
            if _scene_data.get("landmarks"):
                landmarks = _scene_data["landmarks"]

    storyboard = _build_storyboard(book_slug, city, landmarks, cultural, nature)

    if cache_dir:
        storyboard.save(cache_dir / f"{book_slug}_storyboard.json")

    return storyboard


# ── Internal helpers ───────────────────────────────────────────────────────────

def _extract_city(book: BookRecord) -> str:
    for key in ("city", "City", "theme", "Theme", "location", "Location"):
        value = book.raw.get(key)
        if value and str(value).strip() and str(value).strip().lower() != "nan":
            return str(value).strip().title()
    for sep in ("—", "–", "-", ":"):
        if sep in book.title:
            candidate = book.title.split(sep)[-1].strip()
            if candidate:
                return candidate
    return book.title.strip() or "Unknown City"


def _get_field(book: BookRecord, key: str, default: str) -> str:
    value = book.raw.get(key, default)
    if value and str(value).strip() and str(value).strip().lower() != "nan":
        return str(value).strip()
    return default


def _load_city_scenes(book_slug: str) -> list[dict] | None:
    """Load hand-crafted scene descriptions from data/city_scenes/<slug>_scenes.json if it exists."""
    path = _CITY_SCENES_DIR / f"{book_slug}_scenes.json"
    if path.exists():
        data = json.loads(path.read_text())
        return data.get("scenes", [])
    return None


def _build_storyboard(book_slug: str, city: str, landmarks: str, cultural: str, nature: str = "") -> Storyboard:
    city_scenes = _load_city_scenes(book_slug)

    if city_scenes:
        # Use hand-crafted city-specific scenes for rich, unique descriptions
        pages = []
        for entry in city_scenes:
            num = entry["page"]
            cat = entry["category"]
            scene = entry["scene_description"]
            background = entry.get("background", "")
            pose_hint = entry.get("pose", "")
            forbidden = entry.get("forbidden_backgrounds", "")
            prompt = _interior_prompt(scene, city, pose_hint, background, forbidden, book_slug)
            pages.append(PageConcept(page_number=num, scene_category=cat, scene_description=scene, image_prompt=prompt))
    else:
        # Fall back to generic arc with element substitution
        elements = _assign_elements(landmarks, cultural, nature)
        elements["city"] = city
        pages = []
        for num, cat, template, pose_hint in _ARC:
            try:
                scene = template.format(**elements)
            except KeyError:
                scene = template.format(city=city)
            prompt = _interior_prompt(scene, city, pose_hint, "", "", book_slug)
            pages.append(PageConcept(page_number=num, scene_category=cat, scene_description=scene, image_prompt=prompt))

    cover_prompt = _cover_prompt(city, landmarks, book_slug)
    return Storyboard(book_slug=book_slug, city=city, cover_prompt=cover_prompt, pages=pages)


def _interior_prompt(
    scene: str, city: str, pose_hint: str = "",
    background: str = "", forbidden_backgrounds: str = "", book_slug: str = ""
) -> str:
    # Structure: Character Lock → Style Lock → Scene (per brand tip for best consistency)
    character_block = build_character_block(book_slug or city.lower().replace(" ", "_"))

    background_instruction = ""
    if background:
        background_instruction = (
            f"EXACT BACKGROUND FOR THIS PAGE (show ONLY this setting, nothing else): {background}. "
        )
    if forbidden_backgrounds:
        background_instruction += f"DO NOT show: {forbidden_backgrounds}. "
    elif background:
        background_instruction += (
            f"Do NOT add any other {city} landmark not listed above. "
            f"If the Rialto Bridge / Eiffel Tower / Tokyo Tower is not in the exact background above, "
            f"it must NOT appear in this image. "
        )

    return (
        f"{character_block}\n\n"
        f"{background_instruction}"
        f"SCENE: {scene}. "
        f"COMPOSITION: {pose_hint}. "
        f"{_INTERIOR_RULES} "
        f"Overall feel: cozy, calming, emotionally comforting, wholesome kawaii, "
        f"suitable for a premium Amazon KDP coloring book."
    )


def _cover_prompt(city: str, landmarks: str, book_slug: str = "") -> str:
    landmark_detail = f"{landmarks}" if landmarks else f"iconic {city} landmarks"
    character_block = build_cover_character_block(book_slug or city.lower().replace(" ", "_"))

    # CRITICAL: Override model's Japan/Tokyo default with EXPLICIT city name repetition at the start
    _japan_cities = {"tokyo", "kyoto", "osaka", "japan", "nara"}
    is_japan = city.lower() in _japan_cities

    if not is_japan:
        city_lock = (
            f"CRITICAL INSTRUCTION — THIS COVER DEPICTS {city.upper()}, NOT TOKYO OR JAPAN.\n"
            f"The setting is {city}. The city is {city}. The background is {city}. "
            f"The title text must say '{city}' on the cover banner. "
            f"This book is about {city}, not Tokyo or Japan.\n"
            f"FORBIDDEN: Tokyo Tower, cherry blossoms, Japanese temples, torii gates, "
            f"pagodas, Shibuya, Akihabara, Mount Fuji, geishas, Japanese language signs, "
            f"Japanese architecture of any kind, Japanese people, Japanese style, anything Japanese.\n"
            f"REQUIRED: Only {city} landmarks, {city} culture, {city} architecture, {city} atmosphere.\n"
        )
    else:
        city_lock = ""

    _color_hints = {
        "reykjavik": "icy blues, aurora greens, warm cream, colorful corrugated iron house facades in red, blue, yellow, green",
        "iceland": "icy blues, aurora greens, warm cream, colorful corrugated iron house facades in red, blue, yellow, green",
        "venice": "warm terracotta, cream, pale canal blue, dusty rose, red-white striped gondolier",
        "new york city": "sky blue, warm cream, grey-beige, yellow taxi colors, NYC urban energy",
        "mexico city": "vibrant marigold orange, terracotta red, warm cream, bold Mexican folk-art colors",
        "cairo": "warm golden sand, dusty terracotta, sky blue, pharaonic gold, ancient Egypt warmth",
        "egypt": "warm golden sand, dusty terracotta, sky blue, pharaonic gold, ancient Egypt warmth",
    }
    color_palette = _color_hints.get(city.lower(), "soft pastel palette — warm cream, dusty pink, sage green, sky blue")

    return (
        f"{city_lock}"
        f"{character_block}\n\n"
        f"COVER TITLE TEXT — render exactly as specified, centered in a soft cream banner:\n"
        f"Line 1: 'Capybara Adventures' — bold playful font, dark brown\n"
        f"Line 2: '{city}' (THIS LINE MUST SAY '{city}', NOT TOKYO) — LARGEST, bold\n"
        f"Line 3: 'Coloring Books' — smaller\n\n"
        f"BACKGROUND LANDMARKS — render ONLY these {city} landmarks, nothing else:\n"
        f"{landmark_detail}\n\n"
        f"SCENE: Capybara mascot stands confidently in center-foreground, waving one paw cheerfully. "
        f"1–2 small cute companion animals near the mascot's feet. "
        f"The background is pure {city} — if it looks even slightly Japanese or like a different city, "
        f"you have failed the task. "
        f"Color palette: {color_palette}. "
        f"Soft watercolor-gouache children's book cover style."
    )
