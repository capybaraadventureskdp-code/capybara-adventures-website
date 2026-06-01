"""Placeholder image provider — creates white PNGs with page info, no API needed."""

from pathlib import Path
import textwrap

from PIL import Image, ImageDraw

from .base import ImageProvider


class StubProvider(ImageProvider):
    """Creates a white placeholder PNG (8.5 × 11 in at 150 DPI) with the prompt preview."""

    WIDTH = 1275   # 8.5 × 150
    HEIGHT = 1650  # 11  × 150

    @property
    def name(self) -> str:
        return "stub"

    def generate(self, prompt: str, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        img = Image.new("RGB", (self.WIDTH, self.HEIGHT), color="white")
        draw = ImageDraw.Draw(img)

        # Outer border
        draw.rectangle([20, 20, self.WIDTH - 20, self.HEIGHT - 20], outline="#cccccc", width=4)

        # Centered placeholder label
        draw.text(
            (self.WIDTH // 2, self.HEIGHT // 2 - 50),
            "[PLACEHOLDER IMAGE]",
            fill="#aaaaaa",
            anchor="mm",
        )

        # Prompt preview (first 240 chars, wrapped at 55 chars)
        preview = prompt[:240]
        lines = textwrap.wrap(preview, width=55)
        y = self.HEIGHT // 2 + 10
        for line in lines[:8]:
            draw.text((self.WIDTH // 2, y), line, fill="#bbbbbb", anchor="mm")
            y += 26

        img.save(str(output_path), "PNG")
        return output_path
