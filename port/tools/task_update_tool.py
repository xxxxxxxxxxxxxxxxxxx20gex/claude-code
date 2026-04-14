"""TaskUpdate 工具：更新本地任务记录。

可修改标题、描述、状态或元数据，并刷新更新时间。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .common import TASK_STATE_FILE, load_json, save_json, utc_now


class TaskUpdateTool(BaseTool):
    name = "TaskUpdate"
    description = "Update an existing task in the local JSON task store."
    input_schema = {
        "type": "object",
        "properties": {
            "task_id": {"type": "string"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "status": {"type": "string"},
            "metadata": {"type": "object"},
        },
        "required": ["task_id"],
    }

    def run(
        self,
        *,
        task_id: str,
        title: str | None = None,
        description: str | None = None,
        status: str | None = None,
        metadata: dict | None = None,
    ) -> ToolResult:
        state = load_json(TASK_STATE_FILE, {"items": []})
        for task in state.get("items", []):
            if task.get("id") != task_id:
                continue
            if title is not None:
                task["title"] = title
            if description is not None:
                task["description"] = description
            if status is not None:
                task["status"] = status
            if metadata is not None:
                task["metadata"] = metadata
            task["updated_at"] = utc_now()
            save_json(TASK_STATE_FILE, state)
            return self.ok(task, path=str(TASK_STATE_FILE))
        return self.fail(f"Task not found: {task_id}", path=str(TASK_STATE_FILE))


TOOL = TaskUpdateTool()
