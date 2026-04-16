from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from port.config.frontmatter import parse_frontmatter


MAX_MEMORY_FILES = 200


@dataclass(slots=True)
class MemoryHeader:
    filename: str
    file_path: Path
    mtime_ms: float
    description: str | None
    type: str | None


def scan_memory_files(
    memory_dir: Path,
    *,
    max_files: int = MAX_MEMORY_FILES,
) -> list[MemoryHeader]:
    target_dir = Path(memory_dir)
    if not target_dir.exists() or not target_dir.is_dir():
        return []

    headers: list[MemoryHeader] = []
    for file_path in target_dir.rglob("*.md"):
        if file_path.name == "MEMORY.md":
            continue
        parsed = parse_frontmatter(
            file_path.read_text(encoding="utf-8"),
            source_path=str(file_path),
        )
        stat_result = file_path.stat()
        relative_name = file_path.relative_to(target_dir).as_posix()
        description = _coerce_optional_string(parsed.frontmatter.get("description"))
        memory_type = _coerce_optional_string(parsed.frontmatter.get("type"))
        headers.append(
            MemoryHeader(
                filename=relative_name,
                file_path=file_path,
                mtime_ms=stat_result.st_mtime * 1000,
                description=description,
                type=memory_type,
            )
        )

    headers.sort(key=lambda item: item.mtime_ms, reverse=True)
    return headers[:max_files]


def format_memory_manifest(memories: list[MemoryHeader]) -> str:
    lines: list[str] = []
    for memory in memories:
        tag = f"[{memory.type}] " if memory.type else ""
        timestamp = _isoformat_from_mtime(memory.mtime_ms)
        if memory.description:
            lines.append(
                f"- {tag}{memory.filename} ({timestamp}): {memory.description}"
            )
        else:
            lines.append(f"- {tag}{memory.filename} ({timestamp})")
    return "\n".join(lines)


def _coerce_optional_string(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _isoformat_from_mtime(mtime_ms: float) -> str:
    from datetime import datetime, timezone

    return datetime.fromtimestamp(mtime_ms / 1000, tz=timezone.utc).isoformat()

