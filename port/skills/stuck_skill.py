"""stuck 技能：排查本机上疑似卡死或异常缓慢的 Claude Code 会话。"""

from __future__ import annotations

from .base import BaseSkill


class StuckSkill(BaseSkill):
    name = "stuck"
    description = "Investigate frozen or slow Claude Code sessions on this machine."
    user_invocable = True
    source_path = "/home/lyq/claude-code/claude code main/skills/bundled/stuck.ts"

    def get_prompt_text(self) -> str:
        return """# Stuck Skill

诊断本机其他 Claude Code 进程是否处于卡死、挂起、高 CPU 或高内存状态。

## Workflow
1. 枚举 Claude Code 相关进程
2. 找出可疑的 CPU、内存、状态或子进程异常
3. 收集补充证据，例如日志尾部和子进程命令
4. 形成诊断报告

## Rule
只做诊断，不主动 kill 或 signal 任何进程。
"""


SKILL = StuckSkill()
