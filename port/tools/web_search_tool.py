"""WebSearch 工具：执行网页搜索并返回结果列表。

当前通过 DuckDuckGo HTML 搜索页提取标题和链接。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .common import duckduckgo_search


class WebSearchTool(BaseTool):
    name = "WebSearch"
    description = "Search the web and return a compact result list."
    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "max_results": {"type": "integer"},
            "timeout": {"type": "integer"},
        },
        "required": ["query"],
    }

    def run(self, *, query: str, max_results: int = 10, timeout: int = 20) -> ToolResult:
        try:
            results = duckduckgo_search(query, max_results=max_results, timeout=timeout)
        except Exception as exc:
            return self.fail(f"Search failed: {exc}", query=query)
        return self.ok(results, query=query, count=len(results))


TOOL = WebSearchTool()
