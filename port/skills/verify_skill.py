"""verify 技能：验证代码改动是否真的按预期工作。"""

from __future__ import annotations

from .base import BaseSkill


class VerifySkill(BaseSkill):
    name = "verify"
    description = "Verify that a code change actually works by running the app or relevant checks."
    user_invocable = True
    source_path = "/home/lyq/claude-code/claude code main/skills/bundled/verify.ts"
    reference_files = {
        "verify/SKILL.md": "/home/lyq/claude-code/claude code main/skills/bundled/verify/SKILL.md",
        "verify/examples/cli.md": "/home/lyq/claude-code/claude code main/skills/bundled/verify/examples/cli.md",
        "verify/examples/server.md": "/home/lyq/claude-code/claude code main/skills/bundled/verify/examples/server.md",
    }

    def get_prompt_text(self) -> str:
        return """# Verify Skill

验证代码改动是否真正生效，而不仅仅是静态检查通过。

## Workflow
1. 理解改动目标与预期行为
2. 找到可执行的验证路径，例如 CLI、服务端或 UI 流程
3. 运行验证并记录结果
4. 说明是否通过，以及失败时的原因
"""


SKILL = VerifySkill()
