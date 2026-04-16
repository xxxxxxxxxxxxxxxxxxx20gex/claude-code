from __future__ import annotations

from datetime import date
import os
from pathlib import Path
import re
from typing import Mapping


AUTO_MEMORY_DIRNAME = "memory"
AUTO_MEMORY_ENTRYPOINT = "MEMORY.md"
PORT_DISABLE_AUTO_MEMORY_ENV = "CLAUDE_PORT_DISABLE_AUTO_MEMORY"
PORT_MEMORY_BASE_DIR_ENV = "CLAUDE_PORT_MEMORY_BASE_DIR"
PORT_MEMORY_PATH_OVERRIDE_ENV = "CLAUDE_PORT_MEMORY_PATH_OVERRIDE"
UPSTREAM_DISABLE_AUTO_MEMORY_ENV = "CLAUDE_CODE_DISABLE_AUTO_MEMORY"


def is_auto_memory_enabled(
    env: Mapping[str, str] | None = None,
    *,
    default: bool = True,
) -> bool:
    variables = env or os.environ
    for name in (PORT_DISABLE_AUTO_MEMORY_ENV, UPSTREAM_DISABLE_AUTO_MEMORY_ENV):
        value = variables.get(name)
        if value is None:
            continue
        return not _is_truthy(value)
    return default


def get_memory_base_dir(
    memory_base_dir: Path | None = None,
    *,
    env: Mapping[str, str] | None = None,
    home: Path | None = None,
) -> Path:
    if memory_base_dir is not None:
        return Path(memory_base_dir).expanduser().resolve()

    variables = env or os.environ
    env_value = variables.get(PORT_MEMORY_BASE_DIR_ENV)
    if env_value:
        return Path(env_value).expanduser().resolve()

    base_home = home if home is not None else Path.home()
    return (base_home / ".claude").expanduser().resolve()


def get_auto_mem_path(
    project_root: Path,
    memory_base_dir: Path | None = None,
    *,
    env: Mapping[str, str] | None = None,
) -> Path:
    variables = env or os.environ
    override = variables.get(PORT_MEMORY_PATH_OVERRIDE_ENV)
    if override:
        return Path(override).expanduser().resolve()

    base_dir = get_memory_base_dir(memory_base_dir, env=variables)
    sanitized_project = _sanitize_project_root(project_root)
    return base_dir / "projects" / sanitized_project / AUTO_MEMORY_DIRNAME


def get_auto_mem_entrypoint(
    project_root: Path,
    memory_base_dir: Path | None = None,
    *,
    env: Mapping[str, str] | None = None,
) -> Path:
    return get_auto_mem_path(
        project_root,
        memory_base_dir,
        env=env,
    ) / AUTO_MEMORY_ENTRYPOINT


def get_auto_mem_daily_log_path(
    project_root: Path,
    date_value: date | None = None,
    memory_base_dir: Path | None = None,
    *,
    env: Mapping[str, str] | None = None,
) -> Path:
    current_date = date_value or date.today()
    yyyy = f"{current_date.year:04d}"
    mm = f"{current_date.month:02d}"
    dd = f"{current_date.day:02d}"
    return get_auto_mem_path(
        project_root,
        memory_base_dir,
        env=env,
    ) / "logs" / yyyy / mm / f"{yyyy}-{mm}-{dd}.md"


def _is_truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _sanitize_project_root(project_root: Path) -> str:
    normalized = str(Path(project_root).expanduser().resolve())
    sanitized = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    return sanitized or "project"

