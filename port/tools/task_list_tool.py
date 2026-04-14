"""TaskList 工具：列出本地任务记录。

支持按状态过滤，便于快速查看当前任务集合。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .common import TASK_STATE_FILE, load_json


class TaskListTool(BaseTool):
    name = "TaskList"
    description = "List tasks from the local JSON task store."
    input_schema = {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
        },
    }

    def run(self, *, status: str | None = None) -> ToolResult:
        state = load_json(TASK_STATE_FILE, {"items": []})
        items = state.get("items", [])
        if status is not None:
            items = [item for item in items if item.get("status") == status]
        return self.ok(items, count=len(items), path=str(TASK_STATE_FILE))


TOOL = TaskListTool()
