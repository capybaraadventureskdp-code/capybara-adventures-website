"""
Character consistency comparison test.

Generates the same 3 Tokyo scenes across all available providers so you can
visually compare how consistently each AI draws Capy the capybara.

Usage:
    python3 src/test_consistency.py                     # all available providers
    python3 src/test_consistency.py --providers pollinations openai
    python3 src/test_consistency.py --scene 1           # single scene only

Output: output/consistency_test/<provider>/<scene_name>.png
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Make src/ importable when run directly
sys.path.insert(0, str(Path(__file__).parent))

# Load .env from project root
import os
_ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
if _ENV_FILE.exists():
    for _line in _ENV_FILE.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

from character_bible import build_character_block

# ── Three diverse scenes chosen to stress-test character consistency ───────────

TEST_SCENES = [
    {
        "name": "01_arrival",
        "description": (
            "Capy arrives at the Tokyo airport, holding a small rolling suitcase, "
            "looking happy and excited, standing upright"
        ),
        "setting": "Narita International Airport departure hall, gate signs, large windows",
    },
    {
        "name": "02_temple",
        "description": (
            "Capy stands at the base of Senso-ji Temple's giant red lantern gate, "
            "looking up in wonder, one paw raised pointing at the lantern"
        ),
        "setting": "Senso-ji Temple, Asakusa, Tokyo — red lantern gate (Kaminarimon), stone path, cherry blossoms",
    },
    {
        "name": "03_ramen",
        "description": (
            "Capy sits at a small Tokyo ramen counter, holding chopsticks, "
            "looking delighted at a steaming bowl of ramen"
        ),
        "setting": "cozy Tokyo ramen shop interior, wood counter, red paper lanterns, steam rising from bowl",
    },
]

INTERIOR_STYLE = (
    "black-and-white coloring book line art only, thick clean outlines, "
    "no shading, no grayscale, no crosshatching, no dark fills, "
    "large open coloring spaces, minimal details, one clear activity per page, "
    "simple uncluttered composition, lots of white space, soft storybook feeling, "
    "cozy kawaii children's-book style"
)

INTERIOR_RULES = (
    "No humans. No fake text or signage. No crowded scenes. "
    "No tiny unreadable details. White background."
)


def build_scene_prompt(scene: dict) -> str:
    # Structure: Character Lock → Style Lock → Scene (per brand tip)
    character_block = build_character_block("tokyo")
    return (
        f"{character_block}\n\n"
        f"SCENE: {scene['description']}. "
        f"Setting: {scene['setting']}. "
        f"Overall feel: cozy, wholesome kawaii, premium Amazon KDP coloring book page."
    )


def run_test(providers: list[str], scenes: list[dict], output_root: Path) -> None:
    from image_gen import get_provider

    for provider_name in providers:
        print(f"\n{'='*60}")
        print(f"Provider: {provider_name}")
        print(f"{'='*60}")

        try:
            provider = get_provider(provider_name)
        except Exception as exc:
            print(f"  SKIP — could not initialize: {exc}")
            continue

        provider_dir = output_root / provider_name
        provider_dir.mkdir(parents=True, exist_ok=True)

        for scene in scenes:
            out_path = provider_dir / f"{scene['name']}.png"
            if out_path.exists():
                print(f"  {scene['name']}: already exists, skipping")
                continue

            prompt = build_scene_prompt(scene)
            print(f"  Generating {scene['name']}...")
            try:
                provider.generate(prompt, out_path)
                print(f"  ✓ {out_path} ({out_path.stat().st_size // 1024} KB)")
            except Exception as exc:
                print(f"  ✗ {scene['name']} failed: {exc}")

    print(f"\nDone. Review results in: {output_root}")


def detect_available_providers() -> list[str]:
    available = ["pollinations", "huggingface"]  # always free, no key needed
    if os.environ.get("GOOGLE_API_KEY"):
        available.append("gemini")
    if os.environ.get("OPENAI_API_KEY"):
        available.append("openai")
    return available


def main() -> None:
    parser = argparse.ArgumentParser(description="Character consistency test across AI providers.")
    parser.add_argument(
        "--providers", nargs="+",
        help="Providers to test (default: all with API keys set). "
             "Options: pollinations, gemini, openai, stub",
    )
    parser.add_argument(
        "--scene", type=int, choices=[1, 2, 3],
        help="Run only one scene (1=airport, 2=temple, 3=ramen)",
    )
    parser.add_argument(
        "--output-dir", type=Path,
        default=Path(__file__).parents[1] / "output" / "consistency_test",
        help="Where to save comparison images.",
    )
    args = parser.parse_args()

    providers = args.providers or detect_available_providers()
    scenes = [TEST_SCENES[args.scene - 1]] if args.scene else TEST_SCENES

    print(f"Testing providers: {providers}")
    print(f"Scenes: {[s['name'] for s in scenes]}")
    print(f"Output: {args.output_dir}")

    run_test(providers, scenes, args.output_dir)


if __name__ == "__main__":
    main()
