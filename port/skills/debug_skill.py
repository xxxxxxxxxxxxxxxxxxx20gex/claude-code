"""debug 技能：帮助分析当前 Claude Code 会话中的调试信息。"""

from __future__ import annotations

from .base import BaseSkill


class DebugSkill(BaseSkill):
    name = "debug"
    description = "Enable or inspect debug logs for the current session and diagnose issues."
    argument_hint = "[issue description]"
    allowed_tools = ["Read", "Grep", "Glob"]
    user_invocable = True
    disable_model_invocation = True
    source_path = "/home/lyq/claude-code/claude code main/skills/bundled/debug.ts"

    def get_prompt_text(self) -> str:
        return """# Debug Skill

帮助用户诊断当前 Claude Code 会话的问题。

## Workflow
1. 获取当前会话的 debug log 路径
2. 读取日志尾部和关键错误/警告
3. 结合用户描述判断问题成因
4. 给出可操作的修复建议或排查路径
"""


SKILL = DebugSkill()
