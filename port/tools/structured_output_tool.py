"""StructuredOutput 工具：返回结构化内容而不产生副作用。

适合把处理结果封装成统一的数据结构输出。
"""

from __future__ import annotations

from typing import Any

from .base import BaseTool, ToolResult


class StructuredOutputTool(BaseTool):
    name = "StructuredOutput"
    description = "Return structured content without side effects."
    input_schema = {
        "type": "object",
        "properties": {
            "content": {},
            "summary": {"type": "string"},
        },
    }

    def run(self, *, content: Any = None, summary: str | None = None) -> ToolResult:
        return self.ok({"summary": summary, "content": content})


TOOL = StructuredOutputTool()
