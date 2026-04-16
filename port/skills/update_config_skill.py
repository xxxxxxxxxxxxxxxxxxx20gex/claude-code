"""update-config 技能：帮助生成或修改 Claude Code 配置。"""

from __future__ import annotations

from .base import BaseSkill


class UpdateConfigSkill(BaseSkill):
    name = "update-config"
    description = "Help update Claude Code settings, permissions, hooks, and related config."
    allowed_tools = ["Read"]
    user_invocable = True
    source_path = "/home/lyq/claude-code/claude code main/skills/bundled/updateConfig.ts"

    def get_prompt_text(self) -> str:
        return """# Update Config Skill

指导用户修改 Claude Code 的配置文件。

## Focus
- settings.json 层级和作用域
- permissions 规则格式
- hooks 结构与事件
- 模型、环境变量、插件和 MCP 相关配置
"""


SKILL = UpdateConfigSkill()
