"""Google Imagen 4 image generation provider via Google AI Studio.

Requires a Google AI Studio API key with billing enabled: https://aistudio.google.com
Set GOOGLE_API_KEY env var or pass api_key= directly.
Cost: ~$0.01–$0.02 per image (Imagen 4 Fast).

NOTE: Free tier quota for image generation is 0 — billing must be enabled.
"""

import io
import os
from pathlib import Path

from .base import ImageProvider


class GeminiProvider(ImageProvider):
    """Generate images with Google Imagen 4 Fast (requires billing-enabled API key)."""

    # Use Fast for speed/cost; swap to "imagen-4.0-generate-001" for max quality
    MODEL = "imagen-4.0-fast-generate-001"
    # Closest supported ratio to 8.5×11 (0.773); 3:4 = 0.75
    ASPECT_RATIO = "3:4"

    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key or os.environ.get("GOOGLE_API_KEY", "")
        if not self._api_key:
            raise ValueError(
                "GOOGLE_API_KEY is not set.\n"
                "Get a key at https://aistudio.google.com then:\n"
                "  export GOOGLE_API_KEY=your_key_here\n"
                "Note: billing must be enabled on your Google Cloud account."
            )

    @property
    def name(self) -> str:
        return "gemini"

    def generate(self, prompt: str, output_path: Path) -> Path:
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise ImportError(
                "google-genai is required.  Install with:  pip install google-genai"
            ) from exc

        from PIL import Image

        output_path.parent.mkdir(parents=True, exist_ok=True)

        client = genai.Client(api_key=self._api_key)
        response = client.models.generate_images(
            model=self.MODEL,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=self.ASPECT_RATIO,
            ),
        )

        img_bytes = response.generated_images[0].image.image_bytes
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # Pad to exact 8.5×11 ratio (add white bars top/bottom if needed)
        target_w, target_h = 1275, 1650  # 8.5×11 at 150 DPI
        img.thumbnail((target_w, target_h), Image.LANCZOS)
        canvas = Image.new("RGB", (target_w, target_h), "white")
        x = (target_w - img.width) // 2
        y = (target_h - img.height) // 2
        canvas.paste(img, (x, y))
        canvas.save(str(output_path), "PNG")
        return output_path
