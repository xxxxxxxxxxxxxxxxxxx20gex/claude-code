"""Write 工具：写入或追加文本文件内容。

支持自动创建父目录，并返回写入目标和字节数信息。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .common import resolve_path, write_text


class WriteTool(BaseTool):
    name = "Write"
    description = "Write or append text content to a file."
    input_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "content": {"type": "string"},
            "append": {"type": "boolean"},
            "create_parents": {"type": "boolean"},
            "encoding": {"type": "string"},
        },
        "required": ["path", "content"],
    }

    def run(
        self,
        *,
        path: str,
        content: str,
        append: bool = False,
        create_parents: bool = True,
        encoding: str = "utf-8",
    ) -> ToolResult:
        target = resolve_path(path)
        write_text(
            target,
            content,
            append=append,
            create_parents=create_parents,
            encoding=encoding,
        )
        return self.ok(
            {
                "path": str(target),
                "bytes_written": len(content.encode(encoding)),
                "append": append,
            }
        )


TOOL = WriteTool()
