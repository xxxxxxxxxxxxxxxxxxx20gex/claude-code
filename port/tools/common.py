from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any


PORT_ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = PORT_ROOT / ".state"
STATE_DIR.mkdir(parents=True, exist_ok=True)

TODO_STATE_FILE = STATE_DIR / "todos.json"
TASK_STATE_FILE = STATE_DIR / "tasks.json"
MESSAGE_LOG_FILE = STATE_DIR / "messages.jsonl"
CRON_STATE_FILE = STATE_DIR / "cron_jobs.json"
WORKTREE_STATE_FILE = STATE_DIR / "worktrees.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip()).strip("-").lower()
    return text or "item"


def resolve_path(path: str, cwd: str | None = None) -> Path:
    candidate = Path(path).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    base = Path(cwd).expanduser().resolve() if cwd else Path.cwd().resolve()
    return (base / candidate).resolve()


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    return Path(path).read_text(encoding=encoding)


def write_text(
    path: str | Path,
    content: str,
    *,
    append: bool = False,
    create_parents: bool = True,
    encoding: str = "utf-8",
) -> Path:
    target = Path(path)
    if create_parents:
        target.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    with target.open(mode, encoding=encoding) as handle:
        handle.write(content)
    return target


def load_json(path: str | Path, default: Any) -> Any:
    target = Path(path)
    if not target.exists():
        return default
    with target.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: str | Path, data: Any) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=True, indent=2)
        handle.write("\n")
    return target


def append_jsonl(path: str | Path, record: dict[str, Any]) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True))
        handle.write("\n")
    return target


def ensure_command(command: str) -> str | None:
    return shutil.which(command)


def run_process(
    command: str | list[str],
    *,
    cwd: str | None = None,
    timeout: int = 120,
    env: dict[str, str] | None = None,
    shell: bool = False,
    executable: str | None = None,
) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=str(resolve_path(cwd) if cwd else Path.cwd()),
        env={**os.environ, **(env or {})},
        timeout=timeout,
        shell=shell,
        executable=executable,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def http_get(url: str, *, timeout: int = 20, headers: dict[str, str] | None = None) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0 Safari/537.36"
            ),
            **(headers or {}),
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def html_to_text(html: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def duckduckgo_search(query: str, *, max_results: int = 10, timeout: int = 20) -> list[dict[str, str]]:
    url = "https://duckduckgo.com/html/?" + urllib.parse.urlencode({"q": query})
    html = http_get(url, timeout=timeout)
    matches = re.findall(
        r'<a[^>]*class="result__a"[^>]*href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    results: list[dict[str, str]] = []
    for href, title_html in matches[:max_results]:
        title = html_to_text(title_html)
        parsed = urllib.parse.urlparse(href)
        actual_url = href
        if "duckduckgo.com" in parsed.netloc:
            query_params = urllib.parse.parse_qs(parsed.query)
            actual_url = query_params.get("uddg", [href])[0]
        results.append({"title": title, "url": actual_url})
    return results


def discover_skills() -> list[Path]:
    roots = [
        Path("/root/.codex/skills"),
        Path("/home/lyq/claude-code/claude code main/skills"),
    ]
    found: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        found.extend(sorted(root.rglob("SKILL.md")))
    return found
