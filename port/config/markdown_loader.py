from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from .frontmatter import parse_frontmatter


@dataclass(slots=True)
class MarkdownConfigEntry:
    file_path: Path
    base_dir: Path
    frontmatter: dict[str, object]
    content: str
    source: str
    error: str | None = None


def extract_description_from_markdown(
    content: str,
    default: str = "Custom item",
) -> str:
    for line in content.splitlines():
        trimmed = line.strip()
        if not trimmed:
            continue
        header_match = re.match(r"^#+\s+(.+)$", trimmed)
        text = header_match.group(1) if header_match else trimmed
        return text if len(text) <= 100 else text[:97] + "..."
    return default


def load_markdown_files_for_subdir(
    subdir: str,
    roots: list[Path],
) -> list[MarkdownConfigEntry]:
    entries: list[MarkdownConfigEntry] = []
    for root in roots:
        target_dir = _resolve_subdir_root(Path(root), subdir)
        if not target_dir.exists() or not target_dir.is_dir():
            continue

        source = _infer_source(target_dir)
        for file_path in sorted(target_dir.rglob("*.md")):
            parsed = parse_frontmatter(
                file_path.read_text(encoding="utf-8"),
                source_path=str(file_path),
            )
            entries.append(
                MarkdownConfigEntry(
                    file_path=file_path,
                    base_dir=target_dir,
                    frontmatter=parsed.frontmatter,
                    content=parsed.content,
                    source=source,
                    error=parsed.error,
                )
            )
    return entries


def _resolve_subdir_root(root: Path, subdir: str) -> Path:
    if root.name == subdir:
        return root
    return root / subdir


def _infer_source(root: Path) -> str:
    resolved = root.expanduser().resolve()
    home_claude_dir = (Path.home() / ".claude").resolve()
    root_text = str(resolved).lower()
    if resolved == home_claude_dir or home_claude_dir in resolved.parents:
        return "user"
    if "claude code main" in root_text:
        return "builtin"
    return "project"

