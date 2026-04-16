"""claude-api 技能：为 Claude API 与 Agent SDK 使用场景提供参考指导。"""

from __future__ import annotations

from .base import BaseSkill


class ClaudeApiSkill(BaseSkill):
    name = "claude-api"
    description = "Help with Claude API and Agent SDK usage, patterns, and references."
    allowed_tools = ["Read", "Grep", "Glob", "WebFetch"]
    user_invocable = True
    source_path = "/home/lyq/claude-code/claude code main/skills/bundled/claudeApi.ts"

    def get_prompt_text(self) -> str:
        return """# Claude API Skill

帮助用户基于 Claude API 或 Agent SDK 实现能力。

## Focus
- 识别用户当前语言或项目环境
- 指向合适的 API/SDK 参考资料
- 回答模型选择、流式输出、工具调用、批处理等问题
- 优先给出可落地的集成建议

## Notes
- 原始 TypeScript 版本还会按语言动态注入参考文档
- Python 端口保留技能元信息与用途说明，未内联全部文档资源
"""


SKILL = ClaudeApiSkill()
