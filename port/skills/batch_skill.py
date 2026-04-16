"""batch 技能：规划并拆分大规模批量改动，适合并行执行。"""

from __future__ import annotations

from .base import BaseSkill


class BatchSkill(BaseSkill):
    name = "batch"
    description = (
        "Research and plan a large-scale change, then execute it in parallel "
        "across isolated worktree agents."
    )
    when_to_use = (
        "当用户想在很多文件上做机械性、大规模、可拆分的改动时使用，"
        "例如迁移、批量重构、统一替换。"
    )
    argument_hint = "<instruction>"
    user_invocable = True
    disable_model_invocation = True
    source_path = "/home/lyq/claude-code/claude code main/skills/bundled/batch.ts"

    def get_prompt_text(self) -> str:
        return """# Batch Skill

将用户的大规模改动需求拆成可并行执行的独立工作单元。

## Goals
- 先做调研，确认影响范围和约束
- 产出清晰的执行计划和工作拆分
- 为每个单元准备可直接交给子代理的说明

## Workflow
1. 研究代码库，确定需要修改的模块、文件和调用点
2. 设计 5-30 个相互独立的工作单元
3. 明确每个单元的验证方式
4. 汇总成统一计划
5. 若后续进入执行阶段，再并行派发给多个 worker
"""


SKILL = BatchSkill()
