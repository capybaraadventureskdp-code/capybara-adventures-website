"""Abstract interface for image generation backends."""

from abc import ABC, abstractmethod
from pathlib import Path


class ImageProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def generate(self, prompt: str, output_path: Path) -> Path:
        """Generate one image and save it to output_path. Returns the saved path."""
        ...
