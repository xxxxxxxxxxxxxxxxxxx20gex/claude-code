"""loop 技能：把一个提示词或命令调度为定期执行任务。"""

from __future__ import annotations

from .base import BaseSkill


class LoopSkill(BaseSkill):
    name = "loop"
    description = "Run a prompt or slash command on a recurring interval."
    when_to_use = "当用户想按固定频率重复执行某件事，例如轮询状态、周期检查或定时命令时使用。"
    argument_hint = "[interval] <prompt>"
    user_invocable = True
    source_path = "/home/lyq/claude-code/claude code main/skills/bundled/loop.ts"

    def get_prompt_text(self) -> str:
        return """# Loop Skill

把输入解析成 `[interval] <prompt>` 并创建周期性任务。

## Workflow
1. 解析时间间隔与实际 prompt
2. 将间隔转换为 cron 表达式
3. 创建 recurring 任务
4. 立即先执行一次，不等待下一次调度触发
"""


SKILL = LoopSkill()
