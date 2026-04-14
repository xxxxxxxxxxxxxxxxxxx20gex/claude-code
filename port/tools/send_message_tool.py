"""SendMessage 工具：写入本地消息信箱记录。

消息会以 JSONL 形式追加到本地邮箱日志文件中。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .common import MESSAGE_LOG_FILE, append_jsonl, utc_now


class SendMessageTool(BaseTool):
    name = "SendMessage"
    description = "Append a message envelope to the local JSONL mailbox."
    input_schema = {
        "type": "object",
        "properties": {
            "to": {"type": "string"},
            "message": {"type": "string"},
            "from_name": {"type": "string"},
        },
        "required": ["to", "message"],
    }

    def run(self, *, to: str, message: str, from_name: str = "system") -> ToolResult:
        record = {
            "to": to,
            "message": message,
            "from": from_name,
            "created_at": utc_now(),
        }
        append_jsonl(MESSAGE_LOG_FILE, record)
        return self.ok(record, path=str(MESSAGE_LOG_FILE))


TOOL = SendMessageTool()
