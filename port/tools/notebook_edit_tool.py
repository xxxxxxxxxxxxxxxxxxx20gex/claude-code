"""NotebookEdit 工具：编辑 Jupyter Notebook 文件。

支持替换单元格、追加单元格以及更新 notebook 元数据。
"""

from __future__ import annotations

import json

from .base import BaseTool, ToolResult
from .common import resolve_path


class NotebookEditTool(BaseTool):
    name = "NotebookEdit"
    description = "Modify a Jupyter notebook by replacing or appending cells."
    input_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "operation": {
                "type": "string",
                "enum": ["replace_cell", "append_cell", "set_metadata"],
            },
            "cell_index": {"type": "integer"},
            "cell_type": {"type": "string", "enum": ["code", "markdown"]},
            "source": {"type": "string"},
            "metadata": {"type": "object"},
        },
        "required": ["path", "operation"],
    }

    def run(
        self,
        *,
        path: str,
        operation: str,
        cell_index: int | None = None,
        cell_type: str = "code",
        source: str = "",
        metadata: dict | None = None,
    ) -> ToolResult:
        target = resolve_path(path)
        if not target.exists():
            return self.fail(f"Notebook not found: {target}")
        notebook = json.loads(target.read_text(encoding="utf-8"))
        cells = notebook.setdefault("cells", [])
        if operation == "replace_cell":
            if cell_index is None or cell_index < 0 or cell_index >= len(cells):
                return self.fail("cell_index out of range", path=str(target))
            cells[cell_index]["cell_type"] = cell_type
            cells[cell_index]["source"] = source.splitlines(keepends=True)
        elif operation == "append_cell":
            cells.append(
                {
                    "cell_type": cell_type,
                    "execution_count": None if cell_type == "code" else None,
                    "metadata": {},
                    "outputs": [] if cell_type == "code" else [],
                    "source": source.splitlines(keepends=True),
                }
            )
        elif operation == "set_metadata":
            notebook["metadata"] = {**notebook.get("metadata", {}), **(metadata or {})}
        else:
            return self.fail(f"Unsupported operation: {operation}")
        target.write_text(json.dumps(notebook, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
        return self.ok({"path": str(target), "cell_count": len(cells), "operation": operation})


TOOL = NotebookEditTool()
