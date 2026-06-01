# Misbranding Prevention Notes — OpenAI API Prompt Issues

Observed in: Capybara Adventures: New York City (first generation)
Date: 2026-05-30

---

## Issue 1 — Realistic animal instead of kawaii mascot

**Affected pages:** NYC pages 2 (Brooklyn Bridge), 4 (diner), 23 (DUMBO waterfront)

**What happened:**
When the scene description focuses heavily on the environment (sitting on a dock,
sitting at a diner counter, waterfront views), OpenAI renders a realistic capybara
animal placed in the scene rather than the kawaii anthropomorphic mascot.
The character lock prompt gets overridden by the strength of the environmental context.
The character appears with no outfit, in a natural animal pose, not upright.

**Root cause:**
The word order matters. When SETTING details come first or are very dominant,
the model anchors to "realistic animal in a place" rather than "kawaii mascot doing an activity."
Also, poses like "sitting on a wall/dock" naturally prompt realistic animal sitting postures.

**Prevention:**
1. Add this FIRST LINE to every prompt, before the character lock:
   ```
   CRITICAL INSTRUCTION: Draw the kawaii ANTHROPOMORPHIC capybara mascot CHARACTER
   from the Capybara Adventures brand. The character is UPRIGHT, wearing a FULL OUTFIT,
   and behaves like a person. DO NOT draw a realistic capybara animal.
   DO NOT draw a nature scene with an animal in it.
   ```
2. The OUTFIT must be referenced explicitly in the SCENE block:
   ```
   "Capy, wearing the NYC hoodie and blue beanie, sits on the dock..."
   ```
   Not just: "Capybara sits on the dock..."
3. Avoid pose descriptions that trigger realistic animal behavior:
   - AVOID: "sits on a wall/dock/floor" (triggers all-fours animal pose)
   - USE: "sits upright like a person on the edge of the dock"
   - AVOID: "relaxes beside the water"
   - USE: "sits cross-legged at the water's edge, holding a snack"

---

## Issue 2 — Face shape drift back to bear/generic animal

**Affected pages:** NYC pages 18 (parade), 24 (stadium)

**What happened:**
Despite the character lock, the face shape drifted back to a rounder, more
bear-like face. The pear shape and mid-face brown snout were lost.

**Root cause:**
When the scene has many complex elements (crowd, stadium, parade balloon),
the model allocates less attention to the fine-grained character face spec.
The character lock gets partially applied but not fully.

**Prevention:**
1. In high-complexity scenes (crowds, stadiums, parades), explicitly repeat:
   ```
   FACE REMINDER: Pear-shaped head, brown snout starting at MID-FACE,
   small nose HIGH above the mouth, cheek fur tufts, tiny embedded ears.
   NOT a round bear face.
   ```
2. Keep complex scene backgrounds SIMPLER — the busier the background,
   the less the model attends to character detail.
3. For scenes with many elements, explicitly say:
   ```
   Keep the background SIMPLIFIED — the character face is the priority.
   ```

---

## Issue 3 — Extraneous shading in backgrounds

**Affected pages:** NYC page 11 (subway windows — dark speed lines), page 20 (High Line — texture lines), page 24 (stadium — arc shading in seats)

**What happened:**
The model added speed/motion lines in subway windows, crosshatch-like texture
in the High Line ground, and concentric arc shading in the stadium seating.
These are not pure line art — they fill coloring spaces the user should color.

**Root cause:**
The model's default coloring-book style still includes some "implied depth"
through light hatching and speed lines, which it treats as "detail" not "shading."

**Prevention:**
Add these lines explicitly to the STYLE block of every interior prompt:
```
NO speed lines. NO motion blur lines. NO dark fills in windows.
NO crosshatching or hatching in ANY element.
NO concentric shading arcs in stadium seats, bleachers, or curved structures.
NO diagonal texture lines in floors, walls, or backgrounds.
If a window is dark in real life, draw only its outline — leave the interior WHITE.
```

---

## General Rule for Future Books

When the scene involves any of these, add a specific override line:
- Water/waterfront → add "character sits UPRIGHT in kawaii mascot pose, outfit fully visible"
- Diner/counter/table → add "character wears full outfit, clearly visible from torso up"
- Stadium/arena → add "background seating shown as clean outlines only, no shading arcs"
- Train/vehicle → add "windows shown as clean outlined rectangles, interior WHITE, no speed lines"
- Parade/crowd → add "crowd simplified to minimal background shapes, character face is the priority"

---

## Issue 4 — Cover background defaults to Tokyo regardless of city

**Observed in:** Iceland cover (first generation)

**What happened:**
Even though the character correctly wore the Iceland outfit (lopapeysa sweater, pompom hat),
the AI generated a Tokyo background (Tokyo Tower, cherry blossoms, Akihabara signs)
and titled it "Tokyo". The city name "Reykjavik" in the prompt was not strong enough
to override the model's strongest prior: kawaii capybara coloring book = Japan/Tokyo.

**Fix that worked:**
1. Add explicit negative instructions at the very top of the cover prompt:
   ```
   CRITICAL SETTING — THIS IS [CITY], NOT JAPAN:
   NO Tokyo Tower. NO cherry blossoms. NO Japanese architecture.
   ```
2. Name the EXACT local landmarks by their proper names (Hallgrímskirkja, NOT just "church")
3. Name the companions explicitly as local species (puffin + Arctic fox, NOT generic animals)
4. Name the specific color palette tied to the city (aurora greens/purples, NOT cherry blossom pink)

**Rule for all non-Japan covers:**
Always prepend: "CRITICAL SETTING — THIS IS [CITY], [COUNTRY]. NOT Japan. NOT Tokyo.
NO cherry blossoms. NO Tokyo Tower. NO Japanese architecture."
