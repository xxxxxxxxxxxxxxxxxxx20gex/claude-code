from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .markdown_loader import (
    extract_description_from_markdown,
    load_markdown_files_for_subdir,
)


@dataclass(slots=True)
class OutputStyleSpec:
    name: str
    description: str
    prompt: str
    source: str
    keep_coding_instructions: bool | None = None


def load_output_styles(roots: list[Path]) -> list[OutputStyleSpec]:
    styles: list[OutputStyleSpec] = []
    for entry in load_markdown_files_for_subdir("output-styles", roots):
        style_name = entry.file_path.stem
        name = str(entry.frontmatter.get("name") or style_name)
        description = _coerce_description(entry.frontmatter.get("description"))
        if not description:
            description = extract_description_from_markdown(
                entry.content,
                default=f"Custom {style_name} output style",
            )
        keep_coding = _coerce_optional_bool(
            entry.frontmatter.get("keep-coding-instructions")
        )
        styles.append(
            OutputStyleSpec(
                name=name,
                description=description,
                prompt=entry.content.strip(),
                source=entry.source,
                keep_coding_instructions=keep_coding,
            )
        )
    return styles


def _coerce_description(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _coerce_optional_bool(value: object) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
    return None

