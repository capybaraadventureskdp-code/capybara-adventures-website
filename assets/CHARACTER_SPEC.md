# Capybara Adventures — Official Character Specification

**Version:** 1.0 (locked from cover_tokyo_v4.png)  
**Approved:** 2026-05-29  
**Reference image:** `output/consistency_test/openai/cover_tokyo_v4.png`

This document is the single source of truth for generating the Capybara Adventures mascot
consistently across all cover pages and interior coloring pages.

---

## WHAT WORKED — v4 COVER KEY DECISIONS

After iterating through multiple versions, the following specific design decisions produced
the approved capybara character that is clearly distinguishable from a bear or teddy:

1. **Pear-shaped head** — NOT round, NOT wide rectangle. Narrow at the forehead, wider at the cheeks.
2. **Brown snout starts at mid-face** — the darker muzzle area begins just below the eyes, occupying the middle-lower face (not just the chin).
3. **Nose sits high on the snout** — clear visible gap between bottom of nose and top of the smile.
4. **Cheek fur tufts** — slightly textured fur on the sides of the face adds to the pear-shaped width.
5. **Very small ears** — partially embedded in the top of the narrow forehead. NOT bear ears.

---

## GENERATION SETTINGS

### Cover pages (full color)
- **Model:** `gpt-image-2`
- **Quality:** `high`
- **Size:** `1024x1024`
- **Provider:** OpenAI API (`OPENAI_API_KEY` in `.env`)
- **Estimated cost:** ~$0.17/image

### Interior coloring pages (B&W line art)
- **Model:** `gpt-image-2`
- **Quality:** `medium`
- **Size:** `1024x1536` (portrait, ~8.5×11 ratio)
- **Provider:** OpenAI API
- **Estimated cost:** ~$0.042/image

---

## PROMPT STRUCTURE (CRITICAL — must follow this order)

```
Character Lock → Style Lock → Scene Description
```

OpenAI follows the FIRST block most reliably.
Always put the character description BEFORE the scene.

### Full prompt template

```
[CHARACTER LOCK BLOCK]

[OUTFIT for this city]

[STYLE LOCK BLOCK — cover or interior]

[TITLE TEXT — covers only]

SCENE: [specific scene description]
```

---

## CHARACTER LOCK (inject at the start of EVERY prompt)

```
Draw the exact recurring Capybara Adventures mascot.
The mascot must clearly read as a CAPYBARA — NOT a bear, NOT a teddy bear, NOT a hamster, NOT a guinea pig.

HEAD SHAPE: Pear-shaped head — narrow at the top (forehead) and wider at the bottom (cheeks and jaw).
The widest point is at the cheeks/muzzle level, NOT the forehead.
This pear silhouette is a defining capybara feature. NOT round or circular like a bear. NOT a wide rectangle.
Think of an inverted teardrop or pear — slim crown, full wide cheeks.

CHEEK FUR: Slightly longer or textured fur tufts along the sides of the face/cheeks —
like soft sideburns that add to the pear-shaped width at the cheek level.
This cheek fur is a real capybara feature and helps distinguish from bears.

SNOUT/MUZZLE PLACEMENT (CRITICAL): The darker brown snout area begins HIGH on the face —
starting at approximately the MID-FACE level, just below the eyes.
It is NOT confined to only the very bottom of the face.
The snout occupies the middle-lower portion of the face, giving the character
that characteristic capybara look where the darker muzzle takes up significant face real estate.
The snout blends naturally into the face — NOT a separate oval patch.

NOSE PLACEMENT: Small triangular nose centered on the upper portion of the snout area —
sitting HIGH, clearly above the mouth with visible space between nose and smile.
The nose must NOT cover or overlap the mouth. Nose is small and simple.

MOUTH: Tiny simple smile clearly visible BELOW the nose with space between them.
Gentle, warm, cozy expression.

EYES: Large but simple rounded eyes, widely spaced, emotionally warm.
Simple white highlight dot. NOT overly shiny anime eyes.

EARS: Small rounded capybara ears — subtle, partially embedded into the top sides of the narrow forehead.
Do NOT draw large circular teddy-bear ears. Ears are small and unobtrusive.

BODY: Soft bean-shaped torso, rounded, short thick legs, small simple paws.
Warm golden tan fur. Head approximately 40% of total height.
Smooth plush-like appearance — no realistic fur texture.

PERSONALITY: Always cheerful, cozy, warm, curious, gentle — never edgy or aggressive.
```

---

## SNOUT TREATMENT BY PAGE TYPE

### Cover pages (full color)
The snout/muzzle area is **visibly darker brown** than the main golden tan fur.
- Main fur: warm golden tan / soft caramel beige
- Snout area: noticeably darker warm brown
- Blends naturally — no hard line boundary
- The darker snout starts just below the eyes and covers the lower-middle face

Prompt addition for covers:
```
FOR COVERS (full color): the snout/muzzle area must be visibly DARKER BROWN
than the main golden tan fur, starting from mid-face (just below eyes) downward.
This darker brown integrates naturally — the boundary is soft, not a sharp line.
```

### Interior coloring pages (B&W line art)
The snout cannot be brown in a B&W page, but it must still be indicated so the reader
knows to color it differently. Use a **light gray fill (approx 15–20% gray)** in the
snout area only — everything else is pure white.

This is intentional design, common in premium coloring books that hint at intended colors.

Prompt addition for interiors:
```
FOR INTERIORS (B&W line art): The snout/muzzle area should be filled with a
VERY LIGHT GRAY (approximately 15% gray / near-white) — just enough to visually
distinguish the snout zone from the pure white of the rest of the face.
All other interior areas remain pure white. The snout boundary is defined with
a clean outline. This light gray hints to the colorist that the snout is a different color.
```

---

## OUTFIT TEMPLATES BY CITY

| City | Outfit |
|------|--------|
| Tokyo | Blue floral kimono with sakura pattern, obi bow belt, small round hat, camera pouch, rolling suitcase with paw-print sticker |
| Venice | Red-and-white striped gondolier shirt, small straw boater hat with ribbon, cozy scarf, camera pouch |
| Paris | Small beret, cream sweater, cozy scarf, travel satchel, camera pouch |
| New York City | NYC hoodie, blue beanie, camera pouch, small backpack |
| Iceland | Cozy Nordic-pattern sweater, warm knit hat with pompom, scarf, camera pouch |
| Default | Cozy travel outfit with destination-appropriate local accessories, small hat, travel satchel or camera pouch |

---

## COVER TITLE FORMAT

Every cover must display exactly these three lines inside a soft cream rounded banner:

```
Line 1: "Capybara Adventures"  — bold, dark brown, playful children's book font
Line 2: "[CITY/COUNTRY/THEME]" — LARGEST text, bold, warm red or cherry-blossom pink
Line 3: "Coloring Books"       — smaller than Line 1, dark brown
```

No other text anywhere in the cover image.

---

## COMPANION ANIMALS

Include 1–2 small cute companion animals per scene:
- Approved: rabbit, cat, bird, duck, fox, panda, turtle, deer, dog
- Size: approximately 1/3 the height of the capybara
- Style: same rounded kawaii design language
- Outfit: simple destination-appropriate clothing
- NO humans ever

---

## NEGATIVE PROMPT (apply to all generations)

Do NOT generate: bear face, teddy bear, hamster, guinea pig, circular head,
large separate muzzle oval patch, big round bear ears, realistic fur, humans,
shading (except light gray snout on interiors), grayscale fills, crosshatching,
text in interior pages, clutter, dark nighttime fills.

---

## CLI COMMANDS

```bash
# Generate one book (cover + 30 pages + PDF)
python3 src/main.py --book tokyo --provider openai --workers 1

# Generate all books
python3 src/main.py --all --provider openai --workers 1

# Test character consistency (3 scenes)
python3 src/test_consistency.py --providers openai --scene 1

# Generate cover only (via Python)
# See: src/image_gen/openai_gen.py — OpenAIProvider(model='gpt-image-2', size='1024x1024', quality='high')
```

---

# REPEATABLE PIPELINE — STEP BY STEP (verified working as of 2026-05-31)

## To generate a new book from scratch:

### Step 1 — Create the city scene file
```
data/city_scenes/<slug>_scenes.json
```
Follow the format in `TEMPLATE_HOW_TO_ADD_A_CITY.md`.

Each scene MUST include:
- `background` — the EXACT unique setting for this page only
- `forbidden_backgrounds` — what the AI must NOT show (prevents repetition)
- `scene_description` — 2-3 sentences with specific props, pose, companion action
- `companion` — a different animal each page

### Step 2 — Run the pipeline
```bash
python3 src/main.py --book <slug> --provider openai --workers 1
```

For pages-only regeneration (keep existing cover):
```bash
python3 src/main.py --book <slug> --provider openai --workers 1 --skip-cover
```

For specific pages only (delete unwanted pages first, pipeline skips existing):
```bash
rm assets/pages/<slug>/<slug>_page_XX.png
python3 src/main.py --book <slug> --provider openai --workers 1 --skip-cover
```

### Step 3 — Audit for misbranded pages
Check pages where the scene has heavy environmental context (waterfront sitting, diner counter).
Omit page numbers confirmed misbranded when building the KDP PDF.

### Step 4 — Build KDP PDF
```bash
python3 -c "
import sys, os, pathlib; sys.path.insert(0, 'src')
# ... see kdp_assembler.py usage in main.py
"
```
Or just re-run the pipeline (it automatically rebuilds PDFs at the end).

---

## KEY PROMPT RULES THAT WORK (hardcoded in character_bible.py)

1. **"CRITICAL: Draw the kawaii ANTHROPOMORPHIC capybara mascot"** — prevents realistic animal
2. **"Capybara FUR IS PURE WHITE in this coloring page"** — prevents tan fill
3. **"EXACT BACKGROUND FOR THIS PAGE: [specific]"** — prevents Rialto Bridge / Tokyo Tower defaulting
4. **"DO NOT show: [forbidden]"** — prevents repeated backgrounds
5. **"NO speed lines, NO dark window fills, NO concentric arc shading"** — prevents shading
6. **Cover anti-default: "THIS IS [CITY], NOT JAPAN. NO Tokyo Tower. NO cherry blossoms."** — prevents Japan-default on covers

## COVER GENERATION (separate from interior)
- Model: gpt-image-2, quality=high, size=1024x1024
- Always include anti-Japan instruction for non-Japan cities
- Name the specific local landmarks and companions explicitly
- Title format: "Capybara Adventures / [CITY] / Coloring Books"
