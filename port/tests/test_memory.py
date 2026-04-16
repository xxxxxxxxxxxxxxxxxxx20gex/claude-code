from __future__ import annotations

from datetime import date
from pathlib import Path
import os
import time

from port.memory.paths import (
    get_auto_mem_daily_log_path,
    get_auto_mem_entrypoint,
    get_auto_mem_path,
    get_memory_base_dir,
    is_auto_memory_enabled,
)
from port.memory.scan import format_memory_manifest, scan_memory_files


def test_auto_memory_path_generation_is_stable(tmp_path: Path) -> None:
    project_root = tmp_path / "demo-project"
    base_dir = tmp_path / "memory-home"

    first = get_auto_mem_path(project_root, base_dir)
    second = get_auto_mem_path(project_root, base_dir)

    assert first == second
    assert first.name == "memory"


def test_auto_memory_daily_log_and_entrypoint_paths(tmp_path: Path) -> None:
    project_root = tmp_path / "demo-project"
    base_dir = tmp_path / "memory-home"

    entrypoint = get_auto_mem_entrypoint(project_root, base_dir)
    daily_log = get_auto_mem_daily_log_path(
        project_root,
        date(2026, 4, 16),
        base_dir,
    )

    assert entrypoint.name == "MEMORY.md"
    assert daily_log.as_posix().endswith("/logs/2026/04/2026-04-16.md")


def test_memory_base_dir_and_enablement_respect_env(tmp_path: Path, monkeypatch) -> None:
    override_dir = tmp_path / "override-base"
    monkeypatch.setenv("CLAUDE_PORT_MEMORY_BASE_DIR", str(override_dir))
    monkeypatch.setenv("CLAUDE_PORT_DISABLE_AUTO_MEMORY", "1")

    assert get_memory_base_dir() == override_dir.resolve()
    assert is_auto_memory_enabled() is False


def test_scan_memory_files_skips_memory_entrypoint_and_sorts(tmp_path: Path) -> None:
    memory_dir = tmp_path / "memory"
    (memory_dir / "nested").mkdir(parents=True)
    (memory_dir / "MEMORY.md").write_text("# Index\n", encoding="utf-8")
    first = memory_dir / "alpha.md"
    second = memory_dir / "nested" / "beta.md"
    first.write_text(
        "---\ndescription: Alpha note\ntype: project\n---\nBody\n",
        encoding="utf-8",
    )
    time.sleep(0.01)
    second.write_text(
        "---\ndescription: Beta note\ntype: reference\n---\nBody\n",
        encoding="utf-8",
    )

    headers = scan_memory_files(memory_dir)

    assert [header.filename for header in headers] == ["nested/beta.md", "alpha.md"]
    assert headers[0].description == "Beta note"
    assert headers[0].type == "reference"


def test_format_memory_manifest_uses_description_and_type(tmp_path: Path) -> None:
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    memory_file = memory_dir / "fact.md"
    memory_file.write_text(
        "---\ndescription: Useful fact\ntype: user\n---\nBody\n",
        encoding="utf-8",
    )

    headers = scan_memory_files(memory_dir)
    manifest = format_memory_manifest(headers)

    assert "[user] fact.md" in manifest
    assert "Useful fact" in manifest

