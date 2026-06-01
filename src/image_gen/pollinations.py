"""Pollinations.ai image generation provider — completely free, no API key needed."""

import io
import re
import threading
import time
import urllib.parse
from pathlib import Path

from .base import ImageProvider

# Pollinations uses a URL-encoded prompt — keep the encoded form under ~1500 chars.
# Raw prompt budget: ~450 chars total. Allocate as:
#   scene description   ~100 chars
#   character capsule   ~200 chars  ← most important for consistency
#   style + rules       ~100 chars
#   setting hint         ~50 chars
_MAX_PROMPT_CHARS = 450

# Condensed character for Pollinations URL budget — must stay under ~170 chars.
_CHARACTER_CAPSULE = (
    "Capybara World Travel mascot: plush kawaii capybara, warm golden tan, "
    "oversized round head, cream muzzle area, small triangular nose, "
    "large black round eyes with white highlights, blush cheeks, bean-shaped body"
)

_STYLE_SUFFIX = (
    "coloring book page, black-and-white line art, bold clean outlines, "
    "no shading, no gray fills, pure white interior, children's book style"
)


class PollinationsProvider(ImageProvider):
    """Generate images via https://pollinations.ai (free, no auth required).

    Uses the Flux model by default. Images are 850×1100 px (8.5×11 in at 100 DPI).
    Long structured prompts are automatically condensed to stay within URL limits.
    """

    BASE_URL = "https://image.pollinations.ai/prompt/{prompt}"
    DEFAULT_WIDTH = 850
    DEFAULT_HEIGHT = 1100
    MIN_DELAY = 3.0  # seconds between requests — Pollinations throttles concurrent use

    def __init__(self, model: str = "flux") -> None:
        self._model = model
        self._last_request: float = 0.0
        self._lock = threading.Lock()

    @property
    def name(self) -> str:
        return "pollinations"

    def generate(self, prompt: str, output_path: Path) -> Path:
        try:
            import requests
        except ImportError as exc:
            raise ImportError(
                "requests is required.  Install with:  pip install requests"
            ) from exc

        output_path.parent.mkdir(parents=True, exist_ok=True)

        compact = _condense(prompt)

        with self._lock:
            elapsed = time.time() - self._last_request
            if elapsed < self.MIN_DELAY:
                time.sleep(self.MIN_DELAY - elapsed)
            self._last_request = time.time()

        encoded = urllib.parse.quote(compact, safe="")
        url = self.BASE_URL.format(prompt=encoded)
        params = {
            "width": self.DEFAULT_WIDTH,
            "height": self.DEFAULT_HEIGHT,
            "model": self._model,
            "seed": abs(hash(compact)) % (2 ** 31),
        }

        response = requests.get(url, params=params, timeout=120)
        response.raise_for_status()

        from PIL import Image
        img = Image.open(io.BytesIO(response.content)).convert("RGB")
        img.save(str(output_path), "PNG")
        return output_path


def _condense(prompt: str) -> str:
    """Reduce a structured multi-line prompt to a URL-safe single-line compact form.

    Priority order for the limited URL budget:
      1. Scene description  (most important for what is drawn)
      2. Character capsule  (critical for Capy consistency)
      3. Outfit hint        (extracted from OUTFIT: line)
      4. Setting hint       (first landmark only)
      5. Style/rules        (abbreviated)
    """
    if len(prompt) <= _MAX_PROMPT_CHARS and "\n" not in prompt:
        return prompt

    scene = _extract_field(prompt, "SCENE")

    # Extract outfit hint from OUTFIT: line in the character block
    outfit_hint = _extract_outfit_hint(prompt)

    # Extract first landmark from SETTING:
    setting_line = _extract_field(prompt, "SETTING")
    landmark_hint = ""
    m = re.search(r"Incorporate[^:]*:\s*([^.;]+)", setting_line)
    if m:
        first_landmark = m.group(1).strip().split(";")[0].strip()
        if first_landmark:
            landmark_hint = f" at {first_landmark}"

    # Assemble: scene + outfit + landmark + character + style
    # Build progressively and truncate at the limit
    parts = [scene]
    if outfit_hint:
        parts.append(outfit_hint)
    if landmark_hint:
        parts.append(landmark_hint)
    parts.append(_CHARACTER_CAPSULE)
    parts.append(_STYLE_SUFFIX)

    compact = ". ".join(p.rstrip(". ") for p in parts if p)
    return compact[:_MAX_PROMPT_CHARS]


def _extract_outfit_hint(text: str) -> str:
    """Find OUTFIT: anywhere in the prompt and return a short version."""
    m = re.search(r"OUTFIT:\s*(.+?)(?:\.\s*The outfit|$)", text, re.DOTALL)
    if not m:
        return ""
    outfit = m.group(1).strip().rstrip(".")
    # Keep first clause only (up to first comma after 20 chars)
    if len(outfit) > 70:
        idx = outfit.find(",", 20)
        outfit = outfit[:idx].strip() if idx != -1 else outfit[:70]
    return outfit


def _extract_field(text: str, field: str) -> str:
    """Return the value of a 'FIELD: ...' line, or '' if not found."""
    for line in text.splitlines():
        if line.startswith(f"{field}:"):
            return line[len(field) + 1:].strip().rstrip(".")
    return text[:200]  # fallback: first 200 chars of raw prompt
