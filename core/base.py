from dataclasses import dataclass
from datetime import datetime


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


@dataclass
class GroupResult:
    group_name: str
    run_id: str
    steps: list[AgentResult]
    final_output: str
    total_duration_ms: int
    success: bool
    error: str | None
