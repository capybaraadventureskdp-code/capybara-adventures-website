"""OpenAI DALL-E 3 / GPT-4o image generation provider.

Requires: pip install openai
Env var:  OPENAI_API_KEY

GPT-4o image generation is notably better than DALL-E 3 at maintaining character
consistency from detailed text descriptions.
"""

import io
from pathlib import Path

from .base import ImageProvider


class OpenAIProvider(ImageProvider):
    """Generate images via OpenAI's gpt-image-1 (GPT-4o) or dall-e-3 model.

    gpt-image-1 (default) gives the best character-description fidelity.
    Images are generated at 1024x1024 then saved as PNG.
    """

    def __init__(self, model: str = "gpt-image-2", size: str = "1024x1536", quality: str = "medium") -> None:
        self._model = model
        self._size = size
        self._quality = quality

    @property
    def name(self) -> str:
        return f"openai-{self._model}"

    def generate(self, prompt: str, output_path: Path) -> Path:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ImportError(
                "openai package is required.  Install with:  pip install openai"
            ) from exc

        import os
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY environment variable is not set.")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        client = OpenAI(api_key=api_key)

        import base64, requests as req

        is_gpt_image = self._model.startswith("gpt-image") or self._model == "chatgpt-image-latest"

        if is_gpt_image:
            # All gpt-image-* models return base64 by default
            response = client.images.generate(
                model=self._model,
                prompt=prompt,
                n=1,
                size=self._size,
                quality=self._quality,
            )
            image_data = response.data[0]
            if getattr(image_data, "b64_json", None):
                img_bytes = base64.b64decode(image_data.b64_json)
            else:
                img_bytes = req.get(image_data.url, timeout=60).content
        else:
            # dall-e-3 returns a URL
            response = client.images.generate(
                model=self._model,
                prompt=prompt,
                n=1,
                size=self._size,
                quality=self._quality,
            )
            img_bytes = req.get(response.data[0].url, timeout=60).content

        from PIL import Image
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img.save(str(output_path), "PNG")
        return output_path
