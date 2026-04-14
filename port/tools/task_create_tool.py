"""TaskCreate 工具：在本地任务存储中创建任务。

新任务会写入 JSON 状态文件，并带上时间戳和唯一 ID。
"""

from __future__ import annotations

from uuid import uuid4

from .base import BaseTool, ToolResult
from .common import TASK_STATE_FILE, load_json, save_json, utc_now


class TaskCreateTool(BaseTool):
    name = "TaskCreate"
    description = "Create a task in a local JSON task store."
    input_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "status": {"type": "string"},
            "metadata": {"type": "object"},
        },
        "required": ["title"],
    }

    def run(
        self,
        *,
        title: str,
        description: str = "",
        status: str = "pending",
        metadata: dict | None = None,
    ) -> ToolResult:
        state = load_json(TASK_STATE_FILE, {"items": []})
        task = {
            "id": str(uuid4()),
            "title": title,
            "description": description,
            "status": status,
            "metadata": metadata or {},
            "created_at": utc_now(),
            "updated_at": utc_now(),
        }
        state["items"].append(task)
        save_json(TASK_STATE_FILE, state)
        return self.ok(task, path=str(TASK_STATE_FILE))


TOOL = TaskCreateTool()
