from __future__ import annotations

from abc import ABC
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class SkillSpec:
    name: str
    description: str
    when_to_use: str | None = None
    argument_hint: str | None = None
    allowed_tools: list[str] = field(default_factory=list)
    user_invocable: bool = True
    disable_model_invocation: bool = False
    source_path: str | None = None
    reference_files: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class BaseSkill(ABC):
    name: str = ""
    description: str = ""
    when_to_use: str | None = None
    argument_hint: str | None = None
    allowed_tools: list[str] = []
    user_invocable: bool = True
    disable_model_invocation: bool = False
    source_path: str | None = None
    reference_files: dict[str, str] = {}

    def spec(self) -> SkillSpec:
        return SkillSpec(
            name=self.name,
            description=self.description,
            when_to_use=self.when_to_use,
            argument_hint=self.argument_hint,
            allowed_tools=list(self.allowed_tools),
            user_invocable=self.user_invocable,
            disable_model_invocation=self.disable_model_invocation,
            source_path=self.source_path,
            reference_files=dict(self.reference_files),
        )

    def build_prompt(self, args: str = "") -> str:
        args = args.strip()
        prompt = self.get_prompt_text()
        if args:
            prompt += f"\n\n## Additional Context\n\n{args}"
        return prompt

    def get_prompt_text(self) -> str:
        return self.description
