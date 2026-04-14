"""Edit 工具：编辑文本文件内容。

支持按字符串替换，或按行范围覆盖指定片段。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .common import resolve_path


class EditTool(BaseTool):
    name = "Edit"
    description = "Edit a text file by string replacement or line-range replacement."
    input_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "old_text": {"type": "string"},
            "new_text": {"type": "string"},
            "start_line": {"type": "integer"},
            "end_line": {"type": "integer"},
            "replacement": {"type": "string"},
            "expected_occurrences": {"type": "integer"},
            "encoding": {"type": "string"},
        },
        "required": ["path"],
    }

    def run(
        self,
        *,
        path: str,
        old_text: str | None = None,
        new_text: str | None = None,
        start_line: int | None = None,
        end_line: int | None = None,
        replacement: str | None = None,
        expected_occurrences: int | None = None,
        encoding: str = "utf-8",
    ) -> ToolResult:
        target = resolve_path(path)
        if not target.exists():
            return self.fail(f"File not found: {target}")
        original = target.read_text(encoding=encoding)

        if old_text is not None:
            occurrences = original.count(old_text)
            if occurrences == 0:
                return self.fail("old_text was not found in the file", path=str(target))
            if expected_occurrences is not None and occurrences != expected_occurrences:
                return self.fail(
                    f"Expected {expected_occurrences} occurrences, found {occurrences}",
                    path=str(target),
                )
            updated = original.replace(old_text, new_text or "")
        elif start_line is not None and end_line is not None:
            lines = original.splitlines()
            start = max(1, start_line)
            end = min(len(lines), end_line)
            new_lines = lines[: start - 1] + (replacement or "").splitlines() + lines[end:]
            updated = "\n".join(new_lines)
            if original.endswith("\n"):
                updated += "\n"
        else:
            return self.fail(
                "Provide either old_text/new_text or start_line/end_line/replacement"
            )

        target.write_text(updated, encoding=encoding)
        return self.ok(
            {
                "path": str(target),
                "updated": True,
                "original_size": len(original),
                "new_size": len(updated),
            }
        )


TOOL = EditTool()
