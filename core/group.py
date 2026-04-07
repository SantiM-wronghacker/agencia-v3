import uuid
from datetime import datetime, timezone

from core.agent import BaseAgent
from core.base import AgentResult, GroupResult

_VALID_MODES = {"pipeline", "parallel", "director"}


class AgentGroup:
    def __init__(self, name: str, agents: list[BaseAgent], mode: str = "pipeline"):
        if mode not in _VALID_MODES:
            raise ValueError(
                f"Modo '{mode}' no válido. Opciones: {', '.join(_VALID_MODES)}"
            )
        self.name = name
        self.agents = agents
        self.mode = mode

    def execute(self, task: str) -> GroupResult:
        run_id = str(uuid.uuid4())
        start_ms = datetime.now(timezone.utc).timestamp() * 1000

        if self.mode == "pipeline" or self.mode == "director":
            steps, final_output, success, error = self._run_pipeline(task, run_id)
        else:
            steps, final_output, success, error = self._run_parallel(task, run_id)

        total_duration_ms = int(
            datetime.now(timezone.utc).timestamp() * 1000 - start_ms
        )
        return GroupResult(
            group_name=self.name,
            run_id=run_id,
            steps=steps,
            final_output=final_output,
            total_duration_ms=total_duration_ms,
            success=success,
            error=error,
        )

    def _run_pipeline(
        self, task: str, run_id: str
    ) -> tuple[list[AgentResult], str, bool, str | None]:
        steps: list[AgentResult] = []
        current_input = task

        for i, agent in enumerate(self.agents):
            result = agent.run(current_input, run_id, step_index=i)
            steps.append(result)
            if result.success:
                current_input = result.output
            else:
                return steps, "", False, result.error

        final_output = steps[-1].output if steps else ""
        return steps, final_output, True, None

    def _run_parallel(
        self, task: str, run_id: str
    ) -> tuple[list[AgentResult], str, bool, str | None]:
        steps = [
            agent.run(task, run_id, step_index=i)
            for i, agent in enumerate(self.agents)
        ]
        final_output = "\n\n---\n\n".join(
            f"[{r.role}]\n{r.output}" for r in steps if r.success
        )
        success = any(r.success for r in steps)
        error = None if success else "Todos los agentes fallaron"
        return steps, final_output, success, error
