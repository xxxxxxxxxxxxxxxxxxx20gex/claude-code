"""WebFetch 工具：抓取网页并提取清洗后的文本内容。

适合读取页面正文，返回精简后的可读文本。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .common import html_to_text, http_get


class WebFetchTool(BaseTool):
    name = "WebFetch"
    description = "Fetch a web page and return cleaned text content."
    input_schema = {
        "type": "object",
        "properties": {
            "url": {"type": "string"},
            "timeout": {"type": "integer"},
            "max_chars": {"type": "integer"},
        },
        "required": ["url"],
    }

    def run(self, *, url: str, timeout: int = 20, max_chars: int = 20000) -> ToolResult:
        try:
            html = http_get(url, timeout=timeout)
        except Exception as exc:
            return self.fail(f"Fetch failed: {exc}", url=url)
        text = html_to_text(html)[:max_chars]
        return self.ok({"url": url, "content": text, "content_length": len(text)})


TOOL = WebFetchTool()
