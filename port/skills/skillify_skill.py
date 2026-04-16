"""skillify 技能：把一次会话中的可复用流程沉淀成 skill。"""

from __future__ import annotations

from .base import BaseSkill


class SkillifySkill(BaseSkill):
    name = "skillify"
    description = "Turn a repeatable workflow from the session into a reusable skill."
    argument_hint = "[description of the process you want to capture]"
    allowed_tools = ["AskUserQuestion", "Write", "Read", "Edit"]
    user_invocable = True
    disable_model_invocation = True
    source_path = "/home/lyq/claude-code/claude code main/skills/bundled/skillify.ts"

    def get_prompt_text(self) -> str:
        return """# Skillify Skill

把当前会话中的重复流程沉淀为新的 skill 规范。

## Workflow
1. 分析本次会话中执行过的流程、输入、步骤和产出
2. 通过提问补齐命名、参数、触发条件和执行方式
3. 生成结构化的 `SKILL.md`
4. 保存到仓库级或用户级 skill 目录
"""


SKILL = SkillifySkill()
