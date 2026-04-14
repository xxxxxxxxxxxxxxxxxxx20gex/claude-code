"""Skill 工具：列出或读取可用的 SKILL.md 文件。

会扫描预设技能目录，返回技能清单或具体技能内容。
"""

from __future__ import annotations

from .base import BaseTool, ToolResult
from .common import discover_skills


class SkillTool(BaseTool):
    name = "Skill"
    description = "List or read available SKILL.md files from known skill roots."
    input_schema = {
        "type": "object",
        "properties": {
            "operation": {"type": "string", "enum": ["list", "read"]},
            "name": {"type": "string"},
        },
        "required": ["operation"],
    }

    def run(self, *, operation: str, name: str | None = None) -> ToolResult:
        skills = discover_skills()
        if operation == "list":
            payload = [{"name": skill.parent.name, "path": str(skill)} for skill in skills]
            return self.ok(payload, count=len(payload))
        if operation == "read":
            if not name:
                return self.fail("name is required for read")
            for skill in skills:
                if skill.parent.name == name:
                    return self.ok(skill.read_text(encoding="utf-8"), path=str(skill), name=name)
            return self.fail(f"Skill not found: {name}")
        return self.fail(f"Unsupported operation: {operation}")


TOOL = SkillTool()
