from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolResult:
    success: bool
    output: str        # lo que el agente lee como resultado
    raw_data: dict | None = None
    error: str | None = None
    tool_name: str = ""
    duration_ms: int = 0


class BaseTool(ABC):
    name: str = ""
    description: str = ""   # el agente lee esto para saber cuándo usarla

    def __init__(self, credentials: dict = None):
        self.credentials = credentials or {}

    @abstractmethod
    def run(self, **kwargs) -> ToolResult:
        ...

    def _success(self, output: str, raw_data: dict = None) -> ToolResult:
        return ToolResult(
            success=True,
            output=output,
            raw_data=raw_data,
            tool_name=self.name,
        )

    def _error(self, error: str) -> ToolResult:
        return ToolResult(
            success=False,
            output="",
            error=error,
            tool_name=self.name,
        )


class ToolRegistry:
    _tools: dict[str, type[BaseTool]] = {}

    @classmethod
    def register(cls, tool_class: type[BaseTool]) -> type[BaseTool]:
        cls._tools[tool_class.name] = tool_class
        return tool_class

    @classmethod
    def get(cls, name: str) -> type[BaseTool] | None:
        return cls._tools.get(name)

    @classmethod
    def list_all(cls) -> list[dict]:
        return [
            {"name": k, "description": v.description}
            for k, v in cls._tools.items()
        ]


def tool(cls: type[BaseTool]) -> type[BaseTool]:
    """Decorator para registrar una tool en el ToolRegistry."""
    return ToolRegistry.register(cls)
