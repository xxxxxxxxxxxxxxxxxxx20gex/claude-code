"""PowerShell 工具：执行 PowerShell 命令。

会优先使用 `pwsh`，不可用时再尝试传统 `powershell`。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .common import ensure_command, run_process


class PowerShellTool(BaseTool):
    name = "PowerShell"
    description = "Run a command with pwsh or powershell when available."
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
        executable = ensure_command("pwsh") or ensure_command("powershell")
        if not executable:
            return self.fail("PowerShell executable not found")
        result = run_process([executable, "-Command", command], cwd=cwd, timeout=timeout)
        return self.ok(result, returncode=result["returncode"])


TOOL = PowerShellTool()
