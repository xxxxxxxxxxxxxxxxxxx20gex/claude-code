from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class ToolResult:
    ok: bool
    content: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class BaseTool(ABC):
    name: str = ""
    description: str = ""
    input_schema: dict[str, Any] = {"type": "object", "properties": {}}

    def spec(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }

    def ok(self, content: Any = None, **metadata: Any) -> ToolResult:
        return ToolResult(ok=True, content=content, metadata=metadata)

    def fail(self, error: str, **metadata: Any) -> ToolResult:
        return ToolResult(ok=False, error=error, metadata=metadata)

    def __call__(self, **kwargs: Any) -> ToolResult:
        return self.run(**kwargs)

    @abstractmethod
    def run(self, **kwargs: Any) -> ToolResult:
        raise NotImplementedError
