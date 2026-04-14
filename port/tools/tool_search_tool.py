"""ToolSearch 工具：搜索已导出的 Python 工具定义。

按工具名和描述做匹配，返回符合条件的工具规格信息。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult


class ToolSearchTool(BaseTool):
    name = "ToolSearch"
    description = "Search exported Python tool definitions by name or description."
    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
        },
        "required": ["query"],
    }

    def run(self, *, query: str) -> ToolResult:
        from .registry import list_tools

        needle = query.strip().lower()
        matches = []
        for tool in list_tools():
            haystack = f"{tool.name} {tool.description}".lower()
            if needle in haystack:
                matches.append(tool.spec())
        return self.ok(matches, query=query, count=len(matches))


TOOL = ToolSearchTool()
