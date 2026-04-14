"""Glob 工具：按 glob 模式查找文件路径。

适合按目录和通配符批量发现候选文件。
"""

from __future__ import annotations

from pathlib import Path

from .base import BaseTool, ToolResult
from .common import resolve_path


class GlobTool(BaseTool):
    name = "Glob"
    description = "Find files by glob pattern."
    input_schema = {
        "type": "object",
        "properties": {
            "pattern": {"type": "string"},
            "root": {"type": "string"},
            "include_hidden": {"type": "boolean"},
        },
        "required": ["pattern"],
    }

    def run(
        self,
        *,
        pattern: str,
        root: str = ".",
        include_hidden: bool = True,
    ) -> ToolResult:
        base = resolve_path(root)
        if not base.exists():
            return self.fail(f"Root path not found: {base}")
        matches = []
        for item in base.glob(pattern):
            relative = item.relative_to(base)
            if not include_hidden and any(part.startswith(".") for part in relative.parts):
                continue
            matches.append(str(item.resolve()))
        matches.sort()
        return self.ok(matches, count=len(matches), root=str(base))


TOOL = GlobTool()
