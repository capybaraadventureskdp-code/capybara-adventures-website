"""Ideogram image generation provider.

Free tier: 10 free slow-queue images/day (no API key needed via web,
but the API requires a key with free credits on signup).

Ideogram advantages:
- Excellent text rendering in images (great for covers with title text)
- Strong style adherence (follows "coloring book line art" reliably)
- Full prompts accepted — no URL length limit

Sign up at ideogram.ai to get an API key with free credits.
Env var: IDEOGRAM_API_KEY
"""

import io
import json
from pathlib import Path

from .base import ImageProvider


class IdeogramProvider(ImageProvider):
    """Generate images via Ideogram API v2."""

    API_URL = "https://api.ideogram.ai/generate"

    def __init__(
        self,
        model: str = "V_2",
        style: str = "ILLUSTRATION",
        aspect_ratio: str = "ASPECT_2_3",  # portrait ~2:3
    ) -> None:
        self._model = model
        self._style = style
        self._aspect_ratio = aspect_ratio

    @property
    def name(self) -> str:
        return "ideogram"

    def generate(self, prompt: str, output_path: Path) -> Path:
        try:
            import requests
        except ImportError as exc:
            raise ImportError("requests is required: pip install requests") from exc

        import os
        api_key = os.environ.get("IDEOGRAM_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "IDEOGRAM_API_KEY is not set. "
                "Sign up at ideogram.ai for free credits, then add to your .env file."
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        headers = {
            "Api-Key": api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "image_request": {
                "prompt": prompt,
                "model": self._model,
                "style_type": self._style,
                "aspect_ratio": self._aspect_ratio,
                "negative_prompt": (
                    "humans, realistic, photorealistic, 3D CGI, shading, grayscale, "
                    "shadows, crosshatching, sketch texture, dark fills, watermark, "
                    "signature, text artifacts, gibberish"
                ),
            }
        }

        response = requests.post(self.API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        data = response.json()
        image_url = data["data"][0]["url"]

        img_bytes = requests.get(image_url, timeout=60).content

        from PIL import Image
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img.save(str(output_path), "PNG")
        return output_path
