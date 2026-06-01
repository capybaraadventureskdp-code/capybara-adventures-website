"""
Capybara World Travel™ — character specification for all image generation.

Source of truth: assets/brand_identity.md
This module converts the brand doc into ready-to-inject prompt strings.
"""

from pathlib import Path

# ── Load the master brand identity doc ────────────────────────────────────────

_BRAND_DOC_PATH = Path(__file__).resolve().parents[1] / "assets" / "brand_identity.md"

def get_brand_identity() -> str:
    """Return the full master brand identity document."""
    if _BRAND_DOC_PATH.exists():
        return _BRAND_DOC_PATH.read_text().strip()
    return ""


# ── CHARACTER LOCK (the proven structure for OpenAI consistency) ──────────────
# Structure: Character Lock → Style Lock → Scene
# This ordering is critical — OpenAI follows the first block most reliably.
#
# Key face observations from the approved cover references (Tokyo, NYC, Venice):
#  - Head is WIDE ROUNDED-RECTANGLE — wider than tall, almost square. NOT a circle.
#  - CHEEK FUR TUFTS — slightly darker/longer fur along the sides of the face,
#    like subtle sideburns. This is the key real-capybara feature that separates
#    it from bears and hamsters.
#  - Cream muzzle AREA is the lower face zone (lighter color), short and wide.
#  - Nose is a small simple oval/triangle — NOT a wide block, NOT a big protrusion.
#  - Ears are VERY SMALL at the top corners of the wide head.

_CHARACTER_LOCK = (
    "CRITICAL: Draw the kawaii ANTHROPOMORPHIC capybara mascot from the Capybara Adventures brand. "
    "The character is UPRIGHT like a person, wearing a FULL OUTFIT, and interacting with the world like a traveler. "
    "DO NOT draw a realistic capybara animal. DO NOT draw a nature scene with an animal placed in it. "
    "The character must clearly read as a CAPYBARA — NOT a bear, NOT a teddy bear, NOT a hamster, NOT a guinea pig. "

    "HEAD SHAPE: Pear-shaped head — narrow at the top (forehead) and wider at the bottom (cheeks and jaw). "
    "The widest point is at the cheeks/muzzle level, NOT the forehead. "
    "This pear silhouette is a defining capybara feature. NOT round or circular like a bear. NOT a wide rectangle. "
    "Think of an inverted teardrop or pear — slim crown, full wide cheeks. "

    "CHEEK FUR: Slightly longer or textured fur tufts along the sides of the face/cheeks — "
    "like soft sideburns that add to the pear-shaped width at the cheek level. "
    "This cheek fur is a real capybara feature and helps distinguish from bears. "

    "SNOUT/MUZZLE PLACEMENT (CRITICAL): The darker brown snout area begins HIGH on the face — "
    "starting at approximately the MID-FACE level, just below the eyes. "
    "It is NOT confined to only the very bottom of the face. "
    "The snout occupies the middle-lower portion of the face, giving the character "
    "that characteristic capybara look where the darker muzzle takes up significant face real estate. "
    "The snout blends naturally into the face — NOT a separate oval patch. "
    "FOR COVERS: snout area is visibly DARKER BROWN than the main golden tan fur, starting from mid-face down. "
    "FOR INTERIORS: snout boundary defined with a clean outline from mid-face down. "

    "NOSE PLACEMENT: Small triangular nose centered on the upper portion of the snout area — "
    "sitting HIGH, clearly above the mouth with visible space between nose and smile. "
    "The nose must NOT cover or overlap the mouth. Nose is small and simple. "

    "MOUTH: Tiny simple smile clearly visible BELOW the nose with space between them. "
    "Gentle, warm, cozy expression. "

    "EYES: Large but simple rounded eyes, widely spaced, emotionally warm. "
    "Simple white highlight dot. NOT overly shiny anime eyes. "

    "EARS: Small rounded capybara ears — subtle, partially embedded into the top sides of the narrow forehead. "
    "Do NOT draw large circular teddy-bear ears. Ears are small and unobtrusive. "

    "BODY: Soft bean-shaped torso, rounded, short thick legs, small simple paws. "
    "Warm golden tan fur. Head approximately 40% of total height. "
    "Smooth plush-like appearance — no realistic fur texture. "

    "PERSONALITY: Always cheerful, cozy, warm, curious, gentle — never edgy or aggressive."
)

# ── Consistency anchor (appended to every prompt) ─────────────────────────────

_CONSISTENCY_ANCHOR = (
    "Maintain exact Capybara World Travel mascot consistency. "
    "Use the established rounded capybara mascot with oversized head, soft bean-shaped body, "
    "large friendly eyes, tiny smile, plush-like appearance, gentle storybook personality, "
    "cozy handcrafted children's illustration aesthetic, simplified shapes, emotional warmth, "
    "consistent recurring brand character design, collectible series visual identity, "
    "signature warm tan fur palette, rounded cream muzzle area, blush cheeks, "
    "tiny triangular nose, and consistent plush-like mascot proportions. "
    "The mascot must look like the exact same recurring character appearing throughout "
    "an entire global travel book series."
)

# ── Interior (coloring page) style block ──────────────────────────────────────

_INTERIOR_STYLE_BLOCK = (
    "OUTPUT FORMAT: PRINTABLE BLACK-AND-WHITE COLORING BOOK PAGE. "
    "This image contains ONLY two values: black (#000000) for all outlines, white (#FFFFFF) for all fills. "
    "There is ZERO color anywhere. ZERO gray anywhere (except the one snout exception below). "
    "ZERO warm beige. ZERO tan. ZERO golden. ZERO cream fills inside any outline. "
    "Think of this as ink lines on white paper — like a coloring book you buy at a store. "

    "CAPYBARA FUR IS PURE WHITE: Even though the capybara has warm golden tan fur in real life, "
    "in this COLORING PAGE the fur is pure white (#FFFFFF) inside the outlines. "
    "Do NOT fill the capybara's body, face, limbs, or clothing with any color or tan tone. "
    "The colorist will add the fur color themselves. "

    "SNOUT EXCEPTION ONLY: The capybara's snout/muzzle area only may have a VERY LIGHT GRAY "
    "(approximately 15% gray) fill to hint at the different color zone. "
    "This is the ONLY non-white fill anywhere in the entire image. "

    "LINE STYLE: Smooth vector-style outlines. Consistent thick line weight. "
    "NO shading, NO shadows, NO crosshatching, NO hatching, NO stippling, NO gradients. "
    "NO speed lines, NO motion blur. "
    "NO dark fills anywhere in the image. "

    "SPECIFIC MATERIAL RULES — these often cause unintended fills: "
    "Colorful buildings/houses: draw as clean outlined shapes, interior PURE WHITE — the colorist adds the color. "
    "Dark clay, mud, volcanic lava, rocks: draw as outlined blob/rock shapes, interior PURE WHITE — not dark gray. "
    "Water, ocean, lakes, steam, fog, mist: draw as simple curved outline lines only, NO gray fills. "
    "Night sky, dark backgrounds, evening sky, nighttime: MUST be pure white interior. "
    "Draw stars as tiny simple outline circles or dots ONLY — do NOT fill the sky with black or dark gray. "
    "Even if the scene is 'nighttime' or 'dark', the background is WHITE with outline star dots, not filled black. "
    "Fireworks in night scenes: draw as simple starburst outline patterns only, interior white, NO fills. "
    "Ice, snow, frost: draw as simple outlined crystal/blob shapes, interior PURE WHITE — not gray. "
    "Reflections in water: draw as simple wavy horizontal lines only, NO gray fills. "
    "Windows showing scenes outside: draw the window frame as clean lines, interior PURE WHITE or simple outline suggestion. "
    "Wood, stone, brick textures: draw with minimal outlines only, NO crosshatch or texture fills. "
    "If any element in real life would be dark or colorful or black, in this coloring page it is PURE WHITE with a black outline — NEVER a filled black or dark area. "

    "NO concentric shading arcs in seats or curved structures. "
    "NO readable text or signs — use simple icons only. "
    "Every area the colorist should fill must be pure white and open."
)

# ── Companion animals ──────────────────────────────────────────────────────────

_COMPANIONS = (
    "COMPANION: Include 1 small cute companion animal (rabbit, cat, bird, duck, fox, "
    "panda, turtle, or deer). Companion is about 1/3 the size of the capybara, "
    "follows the same rounded kawaii design language, wears simple destination clothing, "
    "and looks friendly and supportive. NO humans ever."
)

# ── Per-city outfit templates ──────────────────────────────────────────────────

CITY_OUTFITS: dict[str, str] = {
    "tokyo": (
        "blue floral kimono with sakura pattern, obi bow belt, small round hat, "
        "camera pouch, rolling suitcase with paw-print sticker"
    ),
    "venice": (
        "red-and-white striped gondolier shirt, small straw boater hat with ribbon, "
        "cozy scarf, camera pouch"
    ),
    "paris": (
        "small beret, cream sweater, cozy scarf, travel satchel, camera pouch"
    ),
    "new_york_city": (
        "NYC hoodie, blue beanie, camera pouch, small backpack"
    ),
    "iceland": (
        "cozy Nordic-pattern sweater, warm knit hat with pompom, scarf, camera pouch"
    ),
    "mexico_city": (
        "colorful embroidered floral jacket with bright flower patterns, "
        "wide-brim sun hat decorated with small flowers, camera pouch, "
        "rolling suitcase with cactus sticker and marigold sticker"
    ),
    "egypt": (
        "light linen explorer shirt in sandy beige, khaki cargo shorts, "
        "wide-brim sun hat with chin strap, camera pouch, "
        "rolling suitcase with pyramid sticker and eye-of-horus sticker"
    ),
    "default": (
        "cozy travel outfit with destination-appropriate local accessories, "
        "small hat or headwear, travel satchel or camera pouch, small backpack"
    ),
}


def get_outfit(city_slug: str) -> str:
    key = city_slug.lower().replace(" ", "_").replace("-", "_")
    return CITY_OUTFITS.get(key, CITY_OUTFITS["default"])


def build_character_block(city_slug: str = "") -> str:
    """Interior coloring page block. Order: Character Lock → Style Lock → (Scene injected by caller)."""
    outfit = get_outfit(city_slug) if city_slug else CITY_OUTFITS["default"]
    return (
        f"{_CHARACTER_LOCK} "
        f"OUTFIT: {outfit}. "
        f"{_COMPANIONS} "
        f"{_INTERIOR_STYLE_BLOCK} "
        f"{_CONSISTENCY_ANCHOR}"
    )


def build_cover_character_block(city_slug: str = "") -> str:
    """Cover illustration block. Order: Character Lock → Style Lock → (Scene injected by caller)."""
    outfit = get_outfit(city_slug) if city_slug else CITY_OUTFITS["default"]
    cover_style = (
        "STYLE: Full-color premium illustration. Soft pastel palette — warm cream, soft tan, "
        "dusty pink, sage green, powder blue, soft lavender. "
        "Handcrafted watercolor-gouache aesthetic. Soft matte finish. Gentle lighting. "
        "Cozy bookstore-quality cover art. NOT glossy CGI. NOT photorealistic. "
        "NOT hyper-detailed AI art. Simplified hand-illustrated storybook feel."
    )
    return (
        f"{_CHARACTER_LOCK} "
        f"OUTFIT: {outfit}. "
        f"{cover_style} "
        f"{_CONSISTENCY_ANCHOR}"
    )


# ── Condensed version for URL-limited providers (Pollinations) ────────────────

CAPY_CONDENSED = (
    "Capybara World Travel mascot: plush-toy capybara, upright, chibi kawaii, "
    "warm golden tan fur, oversized round head, wide rounded cheeks, "
    "cream muzzle area, small triangular nose (NOT wide NOT rectangular), "
    "large round black eyes with white highlights, blush cheeks, tiny smile, "
    "small rounded ears, bean-shaped body, short thick legs, tiny paws"
)
