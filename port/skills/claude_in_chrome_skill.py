"""claude-in-chrome 技能：启用浏览器自动化相关能力。"""

from __future__ import annotations

from .base import BaseSkill


class ClaudeInChromeSkill(BaseSkill):
    name = "claude-in-chrome"
    description = (
        "Automate Chrome interactions for browsing, clicking, form filling, "
        "screenshots, and page inspection."
    )
    when_to_use = "当用户希望操作网页、截图、读取控制台日志或进行浏览器自动化时使用。"
    user_invocable = True
    source_path = "/home/lyq/claude-code/claude code main/skills/bundled/claudeInChrome.ts"

    def get_prompt_text(self) -> str:
        return """# Claude In Chrome Skill

启用浏览器自动化工作流。

## Goals
- 在现有 Chrome 会话中打开或切换页面
- 执行点击、表单填写、截图、读取页面与控制台信息
- 在使用浏览器 MCP 工具前先建立正确的操作上下文

## First Step
先获取当前浏览器标签页上下文，再决定后续动作。
"""


SKILL = ClaudeInChromeSkill()
