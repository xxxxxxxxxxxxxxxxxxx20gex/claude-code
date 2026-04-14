"""CronList 工具：列出本地保存的 cron 计划任务记录。

用于查看当前状态文件中的全部计划项。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .common import CRON_STATE_FILE, load_json


class CronListTool(BaseTool):
    name = "CronList"
    description = "List cron-style schedule entries from the local JSON store."
    input_schema = {
        "type": "object",
        "properties": {},
    }

    def run(self) -> ToolResult:
        state = load_json(CRON_STATE_FILE, {"items": []})
        items = state.get("items", [])
        return self.ok(items, count=len(items), path=str(CRON_STATE_FILE))


TOOL = CronListTool()
