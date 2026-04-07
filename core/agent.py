import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from llm import get_llm
from llm.base import LLMUnavailableError
from core.base import AgentResult

if TYPE_CHECKING:
    from memory.db import AgenciaDB
    from memory.context import ContextMemory


class BaseAgent:
    def __init__(
        self,
        role: str,
        task_type: str = "general",
        db: "AgenciaDB | None" = None,
    ):
        self.role = role
        self.task_type = task_type
        self.system_prompt = self._load_template(role)
        self.llm = get_llm(task_type)
        self.db = db
        self.memory: "ContextMemory | None" = None
        if db is not None:
            from memory.context import ContextMemory
            self.memory = ContextMemory(db)
        self._current_step_id: str | None = None

    def _load_template(self, role: str) -> str:
        path = Path("templates") / f"{role}.txt"
        if path.exists():
            return path.read_text(encoding="utf-8")
        return (
            f"Eres un agente especializado en {role}. "
            "Responde de forma clara, estructurada y profesional."
        )

    def run(
        self,
        input: str,
        run_id: str = None,
        step_index: int = 0,
        managed_by_group: bool = False,
    ) -> AgentResult:
        if run_id is None:
            run_id = str(uuid.uuid4())

        timestamp = datetime.now(timezone.utc)
        start_ms = timestamp.timestamp() * 1000

        self._hook_pre_run(run_id, input, step_index, timestamp, managed_by_group)

        # Inject memory context if available
        if self.memory:
            context = self.memory.inject_context(self.role, input)
            user_message = f"\n\n{context}\n\nTarea: {input}" if context else input
        else:
            user_message = input

        try:
            output = self.llm.generate(self.system_prompt, user_message)
            duration_ms = int(datetime.now(timezone.utc).timestamp() * 1000 - start_ms)
            result = AgentResult(
                role=self.role,
                input=input,
                output=output,
                duration_ms=duration_ms,
                timestamp=timestamp,
                run_id=run_id,
                step_index=step_index,
                provider=self.llm.provider_name,
                success=True,
                error=None,
            )
        except Exception as e:
            duration_ms = int(datetime.now(timezone.utc).timestamp() * 1000 - start_ms)
            result = AgentResult(
                role=self.role,
                input=input,
                output="",
                duration_ms=duration_ms,
                timestamp=timestamp,
                run_id=run_id,
                step_index=step_index,
                provider=self.llm.provider_name,
                success=False,
                error=str(e),
            )

        self._hook_post_run(run_id, result, managed_by_group)
        return result

    def _hook_pre_run(
        self,
        run_id: str,
        input: str,
        step_index: int = 0,
        timestamp: datetime = None,
        managed_by_group: bool = False,
    ):
        print(f"[{self.role}] iniciando run {run_id[:8]}...")
        if self.db is not None and not managed_by_group:
            self._current_step_id = str(uuid.uuid4())
            ts = timestamp or datetime.now(timezone.utc)
            self.db.create_run(run_id, self.role, "solo", input[:200])
            self.db.create_step(
                self._current_step_id, run_id, step_index, self.role, input, ts
            )

    def _hook_post_run(self, run_id: str, result: AgentResult, managed_by_group: bool = False):
        print(f"[{self.role}] completado en {result.duration_ms}ms — {result.provider}")
        if self.db is not None and not managed_by_group and self._current_step_id is not None:
            step_id = self._current_step_id
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
            self.db.complete_run(
                run_id,
                result.output,
                result.duration_ms,
                result.success,
                result.error,
            )
