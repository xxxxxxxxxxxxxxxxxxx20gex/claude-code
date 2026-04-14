"""TodoWrite 工具：维护轻量级待办事项列表。

支持新增、替换、清空和查看，结果持久化到本地状态文件。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .common import TODO_STATE_FILE, load_json, save_json, utc_now


class TodoWriteTool(BaseTool):
    name = "TodoWrite"
    description = "Create, replace, or clear a lightweight todo list stored on disk."
    input_schema = {
        "type": "object",
        "properties": {
            "operation": {"type": "string", "enum": ["add", "replace", "clear", "list"]},
            "items": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["operation"],
    }

    def run(self, *, operation: str, items: list[str] | None = None) -> ToolResult:
        payload = load_json(TODO_STATE_FILE, {"updated_at": None, "items": []})
        current_items = payload.get("items", [])
        if operation == "add":
            current_items.extend(items or [])
        elif operation == "replace":
            current_items = list(items or [])
        elif operation == "clear":
            current_items = []
        elif operation != "list":
            return self.fail(f"Unsupported operation: {operation}")
        payload = {"updated_at": utc_now(), "items": current_items}
        save_json(TODO_STATE_FILE, payload)
        return self.ok(payload, path=str(TODO_STATE_FILE))


TOOL = TodoWriteTool()
