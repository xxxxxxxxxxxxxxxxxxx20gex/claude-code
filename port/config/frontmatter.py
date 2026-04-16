from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

import yaml


FRONTMATTER_REGEX = re.compile(r"^---\s*\n([\s\S]*?)\n---\s*\n?")


@dataclass(slots=True)
class ParsedMarkdown:
    frontmatter: dict[str, Any]
    content: str
    error: str | None = None


def parse_frontmatter(markdown: str, source_path: str | None = None) -> ParsedMarkdown:
    match = FRONTMATTER_REGEX.match(markdown)
    if not match:
        return ParsedMarkdown(frontmatter={}, content=markdown)

    frontmatter_text = match.group(1)
    content = markdown[match.end() :]
    location = f" in {source_path}" if source_path else ""

    try:
        parsed = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError as exc:
        return ParsedMarkdown(
            frontmatter={},
            content=markdown,
            error=f"Failed to parse YAML frontmatter{location}: {exc}",
        )

    if not isinstance(parsed, dict):
        return ParsedMarkdown(
            frontmatter={},
            content=content,
            error=f"Frontmatter must be a mapping{location}",
        )

    return ParsedMarkdown(frontmatter=parsed, content=content)

