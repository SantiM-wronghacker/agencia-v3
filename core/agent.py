import uuid
from datetime import datetime, timezone
from pathlib import Path

from llm import get_llm
from llm.base import LLMUnavailableError
from core.base import AgentResult


class BaseAgent:
    def __init__(self, role: str, task_type: str = "general"):
        self.role = role
        self.task_type = task_type
        self.system_prompt = self._load_template(role)
        self.llm = get_llm(task_type)

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
    ) -> AgentResult:
        if run_id is None:
            run_id = str(uuid.uuid4())

        timestamp = datetime.now(timezone.utc)
        start_ms = timestamp.timestamp() * 1000

        self._hook_pre_run(run_id, input)

        try:
            output = self.llm.generate(self.system_prompt, input)
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

        self._hook_post_run(run_id, result)
        return result

    def _hook_pre_run(self, run_id: str, input: str):
        print(f"[{self.role}] iniciando run {run_id[:8]}...")

    def _hook_post_run(self, run_id: str, result: AgentResult):
        print(f"[{self.role}] completado en {result.duration_ms}ms — {result.provider}")
