"""CronDelete 工具：删除本地 cron 计划任务记录。

会从本地 JSON 状态文件中移除指定的计划项。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .common import CRON_STATE_FILE, load_json, save_json


class CronDeleteTool(BaseTool):
    name = "CronDelete"
    description = "Delete a cron-style schedule entry from the local JSON store."
    input_schema = {
        "type": "object",
        "properties": {
            "cron_id": {"type": "string"},
        },
        "required": ["cron_id"],
    }

    def run(self, *, cron_id: str) -> ToolResult:
        state = load_json(CRON_STATE_FILE, {"items": []})
        before = len(state.get("items", []))
        state["items"] = [item for item in state.get("items", []) if item.get("id") != cron_id]
        if len(state["items"]) == before:
            return self.fail(f"Cron entry not found: {cron_id}", path=str(CRON_STATE_FILE))
        save_json(CRON_STATE_FILE, state)
        return self.ok({"deleted": cron_id}, path=str(CRON_STATE_FILE))


TOOL = CronDeleteTool()
