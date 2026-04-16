"""remember 技能：审查自动记忆并提出整理或提升建议。"""

from __future__ import annotations

from .base import BaseSkill


class RememberSkill(BaseSkill):
    name = "remember"
    description = (
        "Review auto-memory entries and propose promotions or cleanup across "
        "memory layers."
    )
    when_to_use = "当用户要审查、整理、提升或清理 auto-memory、CLAUDE.md、CLAUDE.local.md 时使用。"
    user_invocable = True
    source_path = "/home/lyq/claude-code/claude code main/skills/bundled/remember.ts"

    def get_prompt_text(self) -> str:
        return """# Remember Skill

审查多层记忆内容，并提出结构化的整理建议。

## Workflow
1. 收集所有记忆层内容
2. 判断每条 auto-memory 最适合的归宿
3. 找出重复、过期和冲突项
4. 以“提升 / 清理 / 需澄清 / 无需动作”分组输出报告

## Rule
只提出建议，不直接修改文件，除非用户明确批准。
"""


SKILL = RememberSkill()
