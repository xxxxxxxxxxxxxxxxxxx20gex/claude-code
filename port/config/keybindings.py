from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ParsedKeystroke:
    key: str
    ctrl: bool = False
    alt: bool = False
    shift: bool = False
    meta: bool = False
    super: bool = False


@dataclass(slots=True)
class ParsedBinding:
    chord: list[ParsedKeystroke]
    action: str
    context: str | None = None


@dataclass(slots=True)
class KeybindingsLoadResult:
    bindings: list[ParsedBinding] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def parse_keystroke(input: str) -> ParsedKeystroke:
    parts = input.split("+")
    keystroke = ParsedKeystroke(key="")
    for part in parts:
        lower = part.lower()
        if lower in {"ctrl", "control"}:
            keystroke.ctrl = True
        elif lower in {"alt", "opt", "option"}:
            keystroke.alt = True
        elif lower == "shift":
            keystroke.shift = True
        elif lower == "meta":
            keystroke.meta = True
        elif lower in {"cmd", "command", "super", "win"}:
            keystroke.super = True
        elif lower == "esc":
            keystroke.key = "escape"
        elif lower == "return":
            keystroke.key = "enter"
        elif lower == "space":
            keystroke.key = " "
        elif lower == "↑":
            keystroke.key = "up"
        elif lower == "↓":
            keystroke.key = "down"
        elif lower == "←":
            keystroke.key = "left"
        elif lower == "→":
            keystroke.key = "right"
        else:
            keystroke.key = lower
    return keystroke


def parse_chord(input: str) -> list[ParsedKeystroke]:
    if input == " ":
        return [parse_keystroke("space")]
    normalized = input.strip()
    if not normalized:
        return []
    return [parse_keystroke(part) for part in normalized.split()]


def chord_to_display_string(
    chord: list[ParsedKeystroke],
    platform: str = "linux",
) -> str:
    return " ".join(_keystroke_to_display_string(keystroke, platform) for keystroke in chord)


def parse_bindings(blocks: list[dict[str, Any]]) -> list[ParsedBinding]:
    bindings: list[ParsedBinding] = []
    for block in blocks:
        context = block.get("context")
        raw_bindings = block.get("bindings", {})
        if not isinstance(raw_bindings, dict):
            continue
        for key, action in raw_bindings.items():
            if not isinstance(key, str) or not isinstance(action, str):
                continue
            bindings.append(
                ParsedBinding(
                    chord=parse_chord(key),
                    action=action,
                    context=context if isinstance(context, str) else None,
                )
            )
    return bindings


def get_keybindings_path(home: Path | None = None) -> Path:
    base_home = home if home is not None else Path.home()
    return base_home / ".claude" / "keybindings.json"


def load_keybindings(
    path: Path | None = None,
    default_bindings: list[dict[str, Any]] | None = None,
) -> KeybindingsLoadResult:
    default_blocks = default_bindings or []
    default_parsed = parse_bindings(default_blocks)
    target = path or get_keybindings_path()

    if not target.exists():
        return KeybindingsLoadResult(bindings=default_parsed, warnings=[])

    try:
        parsed = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return KeybindingsLoadResult(
            bindings=default_parsed,
            warnings=[f"Failed to parse keybindings JSON: {exc}"],
        )

    if not isinstance(parsed, dict) or "bindings" not in parsed:
        return KeybindingsLoadResult(
            bindings=default_parsed,
            warnings=['keybindings.json must have a "bindings" array'],
        )

    user_blocks = parsed["bindings"]
    if not isinstance(user_blocks, list):
        return KeybindingsLoadResult(
            bindings=default_parsed,
            warnings=['"bindings" must be an array'],
        )

    warnings: list[str] = []
    valid_blocks: list[dict[str, Any]] = []
    for index, block in enumerate(user_blocks):
        if _is_valid_block(block):
            valid_blocks.append(block)
        else:
            warnings.append(
                f"Skipping invalid keybinding block at index {index}: expected object with string context and object bindings"
            )

    merged = [*default_parsed, *parse_bindings(valid_blocks)]
    return KeybindingsLoadResult(bindings=merged, warnings=warnings)


def _is_valid_block(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    context = value.get("context")
    bindings = value.get("bindings")
    return isinstance(context, str) and isinstance(bindings, dict)


def _keystroke_to_display_string(keystroke: ParsedKeystroke, platform: str) -> str:
    parts: list[str] = []
    if keystroke.ctrl:
        parts.append("ctrl")
    if keystroke.alt or keystroke.meta:
        parts.append("opt" if platform == "macos" else "alt")
    if keystroke.shift:
        parts.append("shift")
    if keystroke.super:
        parts.append("cmd" if platform == "macos" else "super")
    parts.append(_key_to_display_name(keystroke.key))
    return "+".join(parts)


def _key_to_display_name(key: str) -> str:
    return {
        "escape": "Esc",
        " ": "Space",
        "tab": "tab",
        "enter": "Enter",
        "backspace": "Backspace",
        "delete": "Delete",
        "up": "↑",
        "down": "↓",
        "left": "←",
        "right": "→",
        "pageup": "PageUp",
        "pagedown": "PageDown",
        "home": "Home",
        "end": "End",
    }.get(key, key)

