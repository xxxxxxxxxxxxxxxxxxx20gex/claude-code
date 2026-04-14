"""CronCreate 工具：创建本地 cron 计划任务记录。

任务会写入本地 JSON 状态文件，便于后续查询或删除。
"""

from __future__ import annotations

from uuid import uuid4

from .base import BaseTool, ToolResult
from .common import CRON_STATE_FILE, load_json, save_json, utc_now


class CronCreateTool(BaseTool):
    name = "CronCreate"
    description = "Create a cron-style schedule entry in a local JSON store."
    input_schema = {
        "type": "object",
        "properties": {
            "schedule": {"type": "string"},
            "command": {"type": "string"},
            "description": {"type": "string"},
            "metadata": {"type": "object"},
        },
        "required": ["schedule", "command"],
    }

    def run(
        self,
        *,
        schedule: str,
        command: str,
        description: str = "",
        metadata: dict | None = None,
    ) -> ToolResult:
        state = load_json(CRON_STATE_FILE, {"items": []})
        item = {
            "id": str(uuid4()),
            "schedule": schedule,
            "command": command,
            "description": description,
            "metadata": metadata or {},
            "created_at": utc_now(),
        }
        state["items"].append(item)
        save_json(CRON_STATE_FILE, state)
        return self.ok(item, path=str(CRON_STATE_FILE))


TOOL = CronCreateTool()
