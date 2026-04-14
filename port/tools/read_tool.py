"""Read 工具：读取文本文件内容。

支持按完整文件返回，也支持按行范围截取结果。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .common import resolve_path


class ReadTool(BaseTool):
    name = "Read"
    description = "Read a text file, optionally returning only a line range."
    input_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "start_line": {"type": "integer"},
            "end_line": {"type": "integer"},
            "encoding": {"type": "string"},
        },
        "required": ["path"],
    }

    def run(
        self,
        *,
        path: str,
        start_line: int | None = None,
        end_line: int | None = None,
        encoding: str = "utf-8",
    ) -> ToolResult:
        target = resolve_path(path)
        if not target.exists():
            return self.fail(f"File not found: {target}")
        text = target.read_text(encoding=encoding)
        lines = text.splitlines()
        if start_line is not None or end_line is not None:
            start = max(1, start_line or 1)
            end = min(len(lines), end_line or len(lines))
            selected = lines[start - 1 : end]
            content = "\n".join(selected)
            return self.ok(content, path=str(target), start_line=start, end_line=end)
        return self.ok(text, path=str(target), line_count=len(lines))


TOOL = ReadTool()
