"""Image generation provider factory.

Usage:
    from image_gen import get_provider
    provider = get_provider("stub")          # no API key, placeholder PNGs
    provider = get_provider("gemini")        # Google Imagen 3 (GOOGLE_API_KEY)
    provider = get_provider("pollinations")  # Pollinations.ai, free, no auth
    provider = get_provider("openai")        # GPT-4o image gen (OPENAI_API_KEY)
    provider = get_provider()                # reads IMAGE_PROVIDER env var, defaults to stub
"""

import os

from .base import ImageProvider
from .stub import StubProvider
from .gemini import GeminiProvider
from .pollinations import PollinationsProvider
from .openai_gen import OpenAIProvider
from .huggingface_gen import HuggingFaceProvider
from .ideogram_gen import IdeogramProvider

__all__ = [
    "ImageProvider",
    "StubProvider",
    "GeminiProvider",
    "PollinationsProvider",
    "OpenAIProvider",
    "HuggingFaceProvider",
    "IdeogramProvider",
    "get_provider",
]

_PROVIDERS: dict[str, type[ImageProvider]] = {
    "stub": StubProvider,
    "gemini": GeminiProvider,
    "pollinations": PollinationsProvider,
    "openai": OpenAIProvider,
    "huggingface": HuggingFaceProvider,
    "ideogram": IdeogramProvider,
}


def get_provider(name: str | None = None) -> ImageProvider:
    """Return an ImageProvider instance by name.

    Falls back to the IMAGE_PROVIDER environment variable, then 'stub'.
    """
    provider_name = (name or os.environ.get("IMAGE_PROVIDER", "stub")).lower().strip()

    cls = _PROVIDERS.get(provider_name)
    if cls is None:
        valid = ", ".join(f"'{k}'" for k in _PROVIDERS)
        raise ValueError(f"Unknown image provider {provider_name!r}. Valid: {valid}.")

    return cls()
