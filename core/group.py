import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from core.agent import BaseAgent
from core.base import AgentResult, GroupResult

if TYPE_CHECKING:
    from memory.db import AgenciaDB

_VALID_MODES = {"pipeline", "parallel", "director"}


class AgentGroup:
    def __init__(
        self,
        name: str,
        agents: list[BaseAgent],
        mode: str = "pipeline",
        db: "AgenciaDB | None" = None,
    ):
        if mode not in _VALID_MODES:
            raise ValueError(
                f"Modo '{mode}' no válido. Opciones: {', '.join(_VALID_MODES)}"
            )
        self.name = name
        self.agents = agents
        self.mode = mode
        self.db = db

    def execute(self, task: str, run_id: str = None) -> GroupResult:
        run_id = run_id or str(uuid.uuid4())
        start_ms = datetime.now(timezone.utc).timestamp() * 1000

        if self.db:
            self.db.create_run(run_id, self.name, self.mode, task[:200])

        if self.mode in ("pipeline", "director"):
            steps, final_output, success, error = self._run_pipeline(task, run_id)
        else:
            steps, final_output, success, error = self._run_parallel(task, run_id)

        total_duration_ms = int(
            datetime.now(timezone.utc).timestamp() * 1000 - start_ms
        )

        group_result = GroupResult(
            group_name=self.name,
            run_id=run_id,
            steps=steps,
            final_output=final_output,
            total_duration_ms=total_duration_ms,
            success=success,
            error=error,
        )

        if self.db:
            self.db.complete_run(
                run_id,
                group_result.final_output,
                group_result.total_duration_ms,
                group_result.success,
                group_result.error,
            )

        return group_result

    def _persist_step(self, run_id: str, result: AgentResult) -> None:
        if not self.db:
            return
        step_id = str(uuid.uuid4())
        self.db.create_step(
            step_id,
            run_id,
            result.step_index,
            result.role,
            result.input,
            result.timestamp,
        )
        self.db.complete_step(
            run_id,
            step_id,
            result.output,
            result.provider,
            result.duration_ms,
            result.success,
            result.error,
        )
        if result.output:
            self.db.save_observation(run_id, step_id, result.output)

    def _run_pipeline(
        self, task: str, run_id: str
    ) -> tuple[list[AgentResult], str, bool, str | None]:
        steps: list[AgentResult] = []
        current_input = task

        for i, agent in enumerate(self.agents):
            result = agent.run(current_input, run_id, step_index=i, managed_by_group=True)
            steps.append(result)
            self._persist_step(run_id, result)
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
            agent.run(task, run_id, step_index=i, managed_by_group=True)
            for i, agent in enumerate(self.agents)
        ]
        for result in steps:
            self._persist_step(run_id, result)

        final_output = "\n\n---\n\n".join(
            f"[{r.role}]\n{r.output}" for r in steps if r.success
        )
        success = any(r.success for r in steps)
        error = None if success else "Todos los agentes fallaron"
        return steps, final_output, success, error
