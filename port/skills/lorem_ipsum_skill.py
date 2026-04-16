"""lorem-ipsum 技能：生成指定 token 数量附近的占位文本。"""

from __future__ import annotations

from .base import BaseSkill


class LoremIpsumSkill(BaseSkill):
    name = "lorem-ipsum"
    description = "Generate lorem ipsum style filler text with an approximate token target."
    argument_hint = "[token_count]"
    user_invocable = True
    source_path = "/home/lyq/claude-code/claude code main/skills/bundled/loremIpsum.ts"

    def get_prompt_text(self) -> str:
        return """# Lorem Ipsum Skill

生成用于测试、占位或演示的伪文本。

## Goals
- 尽量接近目标 token 数
- 返回可直接用于界面或内容测试的自然段文本
"""


SKILL = LoremIpsumSkill()
