from __future__ import annotations

from pathlib import Path

from port.config.frontmatter import parse_frontmatter
from port.config.markdown_loader import (
    extract_description_from_markdown,
    load_markdown_files_for_subdir,
)


def test_parse_frontmatter_with_valid_yaml() -> None:
    parsed = parse_frontmatter("---\nname: Demo\nenabled: true\n---\n# Title\n")

    assert parsed.frontmatter == {"name": "Demo", "enabled": True}
    assert parsed.content == "# Title\n"
    assert parsed.error is None


def test_parse_frontmatter_without_frontmatter() -> None:
    parsed = parse_frontmatter("# Title\n")

    assert parsed.frontmatter == {}
    assert parsed.content == "# Title\n"
    assert parsed.error is None


def test_parse_frontmatter_with_invalid_yaml_returns_error() -> None:
    markdown = "---\nname: [unterminated\n---\n# Title\n"

    parsed = parse_frontmatter(markdown, source_path="broken.md")

    assert parsed.frontmatter == {}
    assert parsed.content == markdown
    assert parsed.error is not None
    assert "broken.md" in parsed.error


def test_extract_description_from_markdown_falls_back_to_first_content_line() -> None:
    content = "\n\n# Output Style\n\nMore details"

    assert extract_description_from_markdown(content) == "Output Style"


def test_load_markdown_files_for_subdir_keeps_source_labels(tmp_path: Path) -> None:
    home = tmp_path / "home"
    user_root = home / ".claude"
    project_root = tmp_path / "project"
    builtin_root = tmp_path / "claude code main"

    for base in (user_root, project_root, builtin_root):
        (base / "output-styles").mkdir(parents=True)

    (user_root / "output-styles" / "user.md").write_text(
        "---\nname: User Style\n---\n# User\n",
        encoding="utf-8",
    )
    (project_root / "output-styles" / "project.md").write_text(
        "# Project\n",
        encoding="utf-8",
    )
    (builtin_root / "output-styles" / "builtin.md").write_text(
        "# Builtin\n",
        encoding="utf-8",
    )

    previous_home = Path.home()
    try:
        import os

        os.environ["HOME"] = str(home)
        entries = load_markdown_files_for_subdir(
            "output-styles",
            [user_root, project_root, builtin_root],
        )
    finally:
        os.environ["HOME"] = str(previous_home)

    names_to_sources = {entry.file_path.stem: entry.source for entry in entries}
    assert names_to_sources == {
        "user": "user",
        "project": "project",
        "builtin": "builtin",
    }

