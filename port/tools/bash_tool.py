"""Bash 工具：执行 bash shell 命令并返回标准输出、错误输出与退出码。

适合运行本地命令行任务，支持指定工作目录和超时时间。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .common import run_process


class BashTool(BaseTool):
    name = "Bash"
    description = "Run a shell command with bash."
    input_schema = {
        "type": "object",
        "properties": {
            "command": {"type": "string"},
            "cwd": {"type": "string"},
            "timeout": {"type": "integer"},
        },
        "required": ["command"],
    }

    def run(
        self,
        *,
        command: str,
        cwd: str | None = None,
        timeout: int = 120,
    ) -> ToolResult:
        result = run_process(command, cwd=cwd, timeout=timeout, shell=True, executable="/bin/bash")
        return self.ok(result, returncode=result["returncode"])


TOOL = BashTool()
