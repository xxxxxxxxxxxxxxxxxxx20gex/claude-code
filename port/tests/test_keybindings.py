from __future__ import annotations

import json
from pathlib import Path

from port.config.keybindings import (
    chord_to_display_string,
    get_keybindings_path,
    load_keybindings,
    parse_bindings,
    parse_chord,
    parse_keystroke,
)
from port.skills.keybindings_help_skill import KeybindingsHelpSkill


def test_parse_keystroke_supports_common_aliases() -> None:
    keystroke = parse_keystroke("ctrl+shift+esc")

    assert keystroke.ctrl is True
    assert keystroke.shift is True
    assert keystroke.key == "escape"


def test_chord_to_display_string_changes_for_macos() -> None:
    chord = parse_chord("alt+down cmd+k")

    assert chord_to_display_string(chord, platform="macos") == "opt+↓ cmd+k"
    assert chord_to_display_string(chord, platform="linux") == "alt+↓ super+k"


def test_parse_bindings_extracts_context_and_actions() -> None:
    parsed = parse_bindings(
        [
            {
                "context": "global",
                "bindings": {
                    "ctrl+k ctrl+s": "openSettings",
                },
            }
        ]
    )

    assert len(parsed) == 1
    assert parsed[0].context == "global"
    assert parsed[0].action == "openSettings"


def test_load_keybindings_merges_defaults_and_user_bindings(tmp_path: Path) -> None:
    keybindings_path = tmp_path / "keybindings.json"
    keybindings_path.write_text(
        json.dumps(
            {
                "bindings": [
                    {
                        "context": "global",
                        "bindings": {"alt+down": "nextItem"},
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = load_keybindings(
        keybindings_path,
        default_bindings=[
            {
                "context": "global",
                "bindings": {"ctrl+k ctrl+s": "openSettings"},
            }
        ],
    )

    assert [binding.action for binding in result.bindings] == [
        "openSettings",
        "nextItem",
    ]
    assert result.warnings == []


def test_load_keybindings_warns_on_invalid_json(tmp_path: Path) -> None:
    keybindings_path = tmp_path / "keybindings.json"
    keybindings_path.write_text("{invalid", encoding="utf-8")

    result = load_keybindings(keybindings_path)

    assert result.bindings == []
    assert result.warnings
    assert "Failed to parse keybindings JSON" in result.warnings[0]


def test_keybindings_help_skill_uses_keybindings_module(tmp_path: Path, monkeypatch) -> None:
    home = tmp_path / "home"
    keybindings_path = get_keybindings_path(home)
    keybindings_path.parent.mkdir(parents=True)
    keybindings_path.write_text(
        json.dumps(
            {
                "bindings": [
                    {
                        "context": "global",
                        "bindings": {"ctrl+k ctrl+s": "openSettings"},
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("HOME", str(home))

    prompt = KeybindingsHelpSkill().get_prompt_text()

    assert str(keybindings_path) in prompt
    assert "合并后共有 1 条绑定" in prompt
    assert "ctrl+k ctrl+s" in prompt

