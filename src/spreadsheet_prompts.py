"""Apply reusable prompt templates to KDP automation spreadsheets."""

from pathlib import Path

import pandas as pd

from prompt_templates import build_prompt_fields


PROMPT_COLUMNS = [
    "interior_prompt",
    "cover_prompt",
    "color_style",
    "story_notes",
    "composition_type",
    "visual_variation_notes",
    "ending_scene_type",
]


def refresh_prompt_columns(spreadsheet_path: Path, output_path: Path | None = None) -> Path:
    """Update prompt-related columns in an Excel spreadsheet."""

    spreadsheet_path = spreadsheet_path.expanduser().resolve()
    output_path = (output_path or spreadsheet_path).expanduser().resolve()

    df = pd.read_excel(spreadsheet_path, engine="openpyxl")
    if df.empty:
        raise ValueError(f"No rows found in {spreadsheet_path}")

    for column in PROMPT_COLUMNS:
        if column not in df.columns:
            df[column] = ""

    for index, row in df.iterrows():
        fields = build_prompt_fields(row.to_dict(), row_number=index + 1)
        for column in PROMPT_COLUMNS:
            df.at[index, column] = getattr(fields, column)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_path, index=False, engine="openpyxl")
    return output_path
