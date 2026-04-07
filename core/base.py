from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tools.base import ToolResult


@dataclass
class ToolCall:
    tool_name: str
    args: dict
    result: "ToolResult"
    timestamp: str
    duration_ms: int


@dataclass
class AgentResult:
    role: str
    input: str
    output: str
    duration_ms: int
    timestamp: datetime
    run_id: str
    step_index: int
    provider: str
    success: bool
    error: str | None
    tool_calls: list[ToolCall] = field(default_factory=list)


@dataclass
class GroupResult:
    group_name: str
    run_id: str
    steps: list[AgentResult]
    final_output: str
    total_duration_ms: int
    success: bool
    error: str | None
