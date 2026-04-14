"""Grep 工具：在文件内容中搜索文本模式。

优先调用 ripgrep，缺失时回退到 Python 内置遍历搜索。
"""

from __future__ import annotations

import re
from pathlib import Path

from .base import BaseTool, ToolResult
from .common import ensure_command, resolve_path, run_process


class GrepTool(BaseTool):
    name = "Grep"
    description = "Search text in files using ripgrep when available."
    input_schema = {
        "type": "object",
        "properties": {
            "pattern": {"type": "string"},
            "root": {"type": "string"},
            "glob": {"type": "string"},
            "ignore_case": {"type": "boolean"},
            "max_results": {"type": "integer"},
        },
        "required": ["pattern"],
    }

    def run(
        self,
        *,
        pattern: str,
        root: str = ".",
        glob: str | None = None,
        ignore_case: bool = False,
        max_results: int = 200,
    ) -> ToolResult:
        base = resolve_path(root)
        if ensure_command("rg"):
            command = ["rg", "-n", "--color", "never", "--hidden"]
            if ignore_case:
                command.append("-i")
            if glob:
                command.extend(["-g", glob])
            command.extend(["-m", str(max_results), pattern, str(base)])
            result = run_process(command, cwd=str(base))
            return self.ok(
                result["stdout"],
                returncode=result["returncode"],
                stderr=result["stderr"],
                command=" ".join(command),
            )

        flags = re.IGNORECASE if ignore_case else 0
        regex = re.compile(pattern, flags)
        hits: list[str] = []
        for candidate in base.rglob(glob or "*"):
            if not candidate.is_file():
                continue
            try:
                text = candidate.read_text(encoding="utf-8")
            except Exception:
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                if regex.search(line):
                    hits.append(f"{candidate}:{line_no}:{line}")
                    if len(hits) >= max_results:
                        return self.ok("\n".join(hits), count=len(hits), root=str(base))
        return self.ok("\n".join(hits), count=len(hits), root=str(base))


TOOL = GrepTool()
