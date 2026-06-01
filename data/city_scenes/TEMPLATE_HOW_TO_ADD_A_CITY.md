# How to Add a New City to the Capybara Adventures Pipeline

## Overview

Each city gets its own `<city_slug>_scenes.json` in this folder.
When that file exists, the pipeline uses its hand-crafted scene descriptions instead of the generic arc.
This guarantees maximum visual diversity and KDP sales quality.

---

## Step 1 — Create the city scenes JSON

Copy this file structure and fill in 30 scenes:

```
data/city_scenes/<city_slug>_scenes.json
```

City slug format: lowercase, underscores. Examples:
- `venice_scenes.json`
- `new_york_city_scenes.json`
- `paris_scenes.json`

## Step 2 — Follow the scene description rules (from Tokyo template)

Each scene_description MUST include all 5 elements:

```
1. EXACT NAMED LOCATION  — specific venue, street, landmark
2. SPECIFIC ACTION/PROPS — what the capybara is doing + what they're holding
3. CAPYBARA POSE/DIRECTION — body angle, which way they face, are they moving?
4. COMPANION ANIMAL + ACTION — what the companion is doing (different animal each page)
5. KEY BACKGROUND DETAIL — 1-2 specific background elements, simplified
```

Length: 2-3 full sentences per scene (50-80 words). More words = more unique images.

## Step 3 — Vary these across all 30 pages (NEVER repeat the same on adjacent pages)

| Element | Must rotate every page |
|---|---|
| Companion animal | bunny, bird, cat, duck, fox, panda, turtle, deer — use each multiple times but not twice in a row |
| Pose direction | left, right, forward, overhead, profile, three-quarter — always different from adjacent pages |
| Background | Different landmark/setting every single page |
| Activity type | eating, exploring, photographing, resting, dancing, crafting, cycling, etc. |
| Scene scale | Mix close-ups, medium shots, wide shots across the 30 pages |

## Step 4 — Add outfit to CITY_OUTFITS in character_bible.py

```python
"venice": (
    "red-and-white striped gondolier shirt, small straw boater hat with ribbon, "
    "cozy scarf, camera pouch"
),
```

## Step 5 — Run the pipeline

```bash
python3 src/main.py --book <city_slug> --provider openai --workers 1
```

The pipeline will:
1. Auto-detect `data/city_scenes/<slug>_scenes.json`
2. Use the hand-crafted descriptions for all 30 pages
3. Generate cover with "Capybara Adventures / [City] / Coloring Books" title
4. Output everything to `output/kdp_ready/<slug>/`

---

## Scene Category Reference (30 pages)

Use these categories in order — they match the narrative arc:

| Page | Category | Tokyo example setting |
|------|----------|----------------------|
| 1 | arrival | Narita Airport arrivals hall |
| 2 | first_glimpse | Sumida River, first view of Tokyo Tower |
| 3 | hotel | Traditional ryokan room |
| 4 | breakfast | Tsukiji market sushi counter |
| 5 | landmark_1 | Base of Tokyo Tower |
| 6 | photo | Senso-ji Kaminarimon Gate |
| 7 | market | Harajuku Takeshita Street stall |
| 8 | street_food | Asakusa taiyaki stall |
| 9 | park | Yoyogi Park cherry blossoms |
| 10 | local_animal | Shiba Inu encounter in park |
| 11 | transport | Shinkansen bullet train window |
| 12 | landmark_2 | Tokyo Skytree observation deck |
| 13 | shopping | Akihabara electronics shop |
| 14 | craft | Harajuku origami workshop |
| 15 | temple | Meiji Shrine torii path |
| 16 | viewpoint | Rooftop overlooking Shibuya |
| 17 | snack | Shimokitazawa matcha café |
| 18 | festival | Tanabata festival |
| 19 | dinner | Shibuya ramen shop |
| 20 | evening_walk | Asakusa Nakamise lane evening |
| 21 | museum | Edo-Tokyo Museum |
| 22 | outdoor | Sumida River cycling path |
| 23 | waterside | Odaiba beach dock, Tokyo Bay |
| 24 | sport | Ryogoku sumo arena |
| 25 | art_market | Kappabashi kitchen street |
| 26 | celebration | Awa Odori dance festival |
| 27 | new_friends | Yoyogi Park group farewell |
| 28 | packing | Ryokan room, departure morning |
| 29 | farewell | Narita Airport departure gate |
| 30 | memories | Floor spread of Tokyo souvenirs |

Replace each Tokyo-specific setting with the equivalent for the new city.

---

## Cover Page Rules (always the same format)

The cover prompt in `storyboard.py` automatically generates:

```
"Capybara Adventures"     ← Line 1, bold dark brown
"[CITY]"                  ← Line 2, LARGEST, warm red/pink
"Coloring Books"          ← Line 3, smaller dark brown
```

Inside a soft cream rounded banner at the top of a full-color illustration.
The AI generates the title text directly in the image — no post-processing needed.

Cover model settings: `gpt-image-2`, quality=`high`, size=`1024x1024`

---

## Capybara Character — Always Identical Across All Books

The character description in `src/character_bible.py` is automatically injected into every prompt.
You do NOT need to copy or edit it per city.

Key features locked in (from v4 approval, 2026-05-29):
- Pear-shaped head (narrow forehead, wide cheeks)
- Darker brown snout starting at mid-face
- Small nose HIGH on snout, clearly above the mouth
- Cheek fur tufts for width
- Very small embedded ears
- Warm golden tan fur
- Bean-shaped body, short thick legs

For B&W interiors: light gray (~15%) snout fill to indicate different color zone.
For covers: full color with visibly darker brown snout.

This is automatically handled — no changes needed per city.
