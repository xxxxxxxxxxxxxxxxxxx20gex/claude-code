"""simplify 技能：审查变更并收敛成更简洁、更高质量的实现。"""

from __future__ import annotations

from .base import BaseSkill


class SimplifySkill(BaseSkill):
    name = "simplify"
    description = "Review changed code for reuse, quality, and efficiency, then improve it."
    user_invocable = True
    source_path = "/home/lyq/claude-code/claude code main/skills/bundled/simplify.ts"

    def get_prompt_text(self) -> str:
        return """# Simplify Skill

审查最近的代码改动，并找出可以简化、复用或提效的地方。

## Review Angles
- 代码复用：是否已有现成工具或抽象
- 代码质量：是否有重复、参数蔓延、抽象泄漏
- 效率：是否存在重复工作、缺少并发、热路径膨胀

## Goal
修正明显问题，或者确认当前改动已经足够简洁。
"""


SKILL = SimplifySkill()
