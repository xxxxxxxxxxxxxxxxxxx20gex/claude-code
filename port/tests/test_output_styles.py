from __future__ import annotations

from pathlib import Path

from port.config import load_output_styles


def test_load_output_styles_from_markdown_files(tmp_path: Path) -> None:
    root = tmp_path / ".claude"
    styles_dir = root / "output-styles"
    styles_dir.mkdir(parents=True)
    (styles_dir / "intentional.md").write_text(
        "---\nname: Intentional\n"
        "description: Purposeful output style\n"
        "keep-coding-instructions: true\n"
        "---\n"
        "Write with sharp edges.\n",
        encoding="utf-8",
    )

    styles = load_output_styles([root])

    assert len(styles) == 1
    style = styles[0]
    assert style.name == "Intentional"
    assert style.description == "Purposeful output style"
    assert style.prompt == "Write with sharp edges."
    assert style.keep_coding_instructions is True
    assert style.source == "project"


def test_load_output_styles_falls_back_to_markdown_description(tmp_path: Path) -> None:
    root = tmp_path / "project"
    styles_dir = root / "output-styles"
    styles_dir.mkdir(parents=True)
    (styles_dir / "compact.md").write_text(
        "## Compact answer style\n\nKeep it short.\n",
        encoding="utf-8",
    )

    styles = load_output_styles([root])

    assert styles[0].name == "compact"
    assert styles[0].description == "Compact answer style"

