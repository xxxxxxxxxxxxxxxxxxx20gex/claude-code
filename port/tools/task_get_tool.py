"""TaskGet 工具：按 ID 读取本地任务记录。

用于从 JSON 任务状态文件中查询单个任务详情。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .common import TASK_STATE_FILE, load_json


class TaskGetTool(BaseTool):
    name = "TaskGet"
    description = "Get a task from the local JSON task store by id."
    input_schema = {
        "type": "object",
        "properties": {
            "task_id": {"type": "string"},
        },
        "required": ["task_id"],
    }

    def run(self, *, task_id: str) -> ToolResult:
        state = load_json(TASK_STATE_FILE, {"items": []})
        for task in state.get("items", []):
            if task.get("id") == task_id:
                return self.ok(task, path=str(TASK_STATE_FILE))
        return self.fail(f"Task not found: {task_id}", path=str(TASK_STATE_FILE))


TOOL = TaskGetTool()
