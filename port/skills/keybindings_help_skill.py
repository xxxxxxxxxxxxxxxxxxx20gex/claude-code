"""keybindings-help 技能：说明和生成 Claude Code 快捷键配置。"""

from __future__ import annotations

from port.config.keybindings import (
    chord_to_display_string,
    get_keybindings_path,
    load_keybindings,
    parse_chord,
)

from .base import BaseSkill


class KeybindingsHelpSkill(BaseSkill):
    name = "keybindings-help"
    description = "Help customize Claude Code keybindings via keybindings.json."
    allowed_tools = ["Read"]
    user_invocable = False
    source_path = "/home/lyq/claude-code/claude code main/skills/bundled/keybindings.ts"

    def get_prompt_text(self) -> str:
        keybindings_path = get_keybindings_path()
        load_result = load_keybindings(keybindings_path)
        examples = [
            chord_to_display_string(parse_chord("ctrl+k ctrl+s")),
            chord_to_display_string(parse_chord("alt+down")),
            chord_to_display_string(parse_chord("space")),
        ]
        status_line = (
            f"已检测到现有配置，合并后共有 {len(load_result.bindings)} 条绑定。"
            if keybindings_path.exists()
            else "尚未检测到现有配置文件，首次创建时请保留对象包装格式。"
        )
        warnings = ""
        if load_result.warnings:
            warning_lines = "\n".join(f"- {warning}" for warning in load_result.warnings)
            warnings = f"\n## Current Warnings\n{warning_lines}\n"

        return f"""# Keybindings Help Skill

用于创建或修改 `~/.claude/keybindings.json`。

## Current State
- 配置路径：`{keybindings_path}`
- {status_line}
{warnings}

## Expectations
- 先读取现有 keybindings 文件，再合并修改
- 说明上下文、动作名和快捷键语法
- 避免覆盖整个文件

## Keybinding Syntax
- 采用 `{{"bindings": [ ... ]}}` 顶层结构
- 每个 block 需要 `context` 和 `bindings`
- chord 示例：`{examples[0]}`、`{examples[1]}`、`{examples[2]}`
- 常见特殊键：`Esc`、`Enter`、`Space`、方向键
"""


SKILL = KeybindingsHelpSkill()
