"""HuggingFace Inference API image generation provider — free tier, no API key required.

Uses FLUX.1-schnell by default (fast, high quality, fully open).
Full prompts accepted — no URL length limit unlike Pollinations.

Optional: set HF_API_KEY env var to increase rate limits.
"""

import io
import time
from pathlib import Path

from .base import ImageProvider


class HuggingFaceProvider(ImageProvider):
    """Generate images via HuggingFace Inference API using FLUX.1-schnell."""

    DEFAULT_MODEL = "black-forest-labs/FLUX.1-schnell"
    API_URL = "https://api-inference.huggingface.co/models/{model}"
    MIN_DELAY = 2.0

    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        self._model = model
        self._last_request: float = 0.0

    @property
    def name(self) -> str:
        return "huggingface"

    def generate(self, prompt: str, output_path: Path) -> Path:
        try:
            import requests
        except ImportError as exc:
            raise ImportError("requests is required: pip install requests") from exc

        import os
        output_path.parent.mkdir(parents=True, exist_ok=True)

        elapsed = time.time() - self._last_request
        if elapsed < self.MIN_DELAY:
            time.sleep(self.MIN_DELAY - elapsed)

        headers = {"Content-Type": "application/json"}
        api_key = os.environ.get("HF_API_KEY") or os.environ.get("HUGGINGFACE_API_KEY")
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        url = self.API_URL.format(model=self._model)
        payload = {
            "inputs": prompt,
            "parameters": {
                "width": 832,
                "height": 1216,
                "num_inference_steps": 4,
            },
        }

        response = requests.post(url, headers=headers, json=payload, timeout=120)
        self._last_request = time.time()

        if response.status_code == 503:
            # Model loading — wait and retry once
            time.sleep(20)
            response = requests.post(url, headers=headers, json=payload, timeout=120)

        response.raise_for_status()

        from PIL import Image
        img = Image.open(io.BytesIO(response.content)).convert("RGB")
        img.save(str(output_path), "PNG")
        return output_path
