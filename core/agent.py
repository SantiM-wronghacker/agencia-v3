import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from llm import get_llm
from llm.base import LLMUnavailableError
from core.base import AgentResult, ToolCall

if TYPE_CHECKING:
    from memory.db import AgenciaDB
    from memory.context import ContextMemory
    from tools.base import BaseTool, ToolResult

MAX_TOOL_CALLS = 3


class BaseAgent:
    def __init__(
        self,
        role: str,
        task_type: str = "general",
        db: "AgenciaDB | None" = None,
        tools: "list[BaseTool] | None" = None,
    ):
        self.role = role
        self.task_type = task_type
        self.system_prompt = self._load_template(role)
        self.llm = get_llm(task_type)
        self.db = db
        self.tools: list = tools or []
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

    # ------------------------------------------------------------------
    # Tools support
    # ------------------------------------------------------------------

    def _build_tools_context(self) -> str:
        if not self.tools:
            return ""
        lines = ["Tienes acceso a estas herramientas:"]
        for t in self.tools:
            lines.append(f"- {t.name}: {t.description}")
        lines.append("\nPara usar una herramienta responde con formato JSON:")
        lines.append('{"use_tool": "nombre_tool", "args": {"param": "valor"}}')
        lines.append("Si no necesitas herramientas responde directamente.")
        return "\n".join(lines)

    def _try_parse_tool_call(self, output: str) -> dict | None:
        from tools.utils.text import extract_json
        data = extract_json(output)
        if data and "use_tool" in data:
            return data
        return None

    def _execute_tool(self, tool_name: str, args: dict) -> "ToolResult":
        from tools.base import ToolResult
        for t in self.tools:
            if t.name == tool_name:
                try:
                    return t.run(**args)
                except Exception as e:
                    return ToolResult(
                        success=False,
                        output="",
                        error=str(e),
                        tool_name=tool_name,
                    )
        from tools.base import ToolResult
        return ToolResult(
            success=False,
            output="",
            error=f"Tool '{tool_name}' no disponible",
            tool_name=tool_name,
        )

    # ------------------------------------------------------------------
    # Main run
    # ------------------------------------------------------------------

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
            base_message = f"\n\n{context}\n\nTarea: {input}" if context else input
        else:
            base_message = input

        # Build tools context once
        tools_context = self._build_tools_context()
        current_input = input
        tool_calls: list[ToolCall] = []

        enhanced_input = (
            f"{base_message}\n\n{tools_context}" if tools_context else base_message
        )

        output = ""
        try:
            for attempt in range(MAX_TOOL_CALLS + 1):
                output = self.llm.generate(self.system_prompt, enhanced_input)

                tool_call_data = self._try_parse_tool_call(output)
                if not tool_call_data or attempt == MAX_TOOL_CALLS:
                    break  # respuesta final, sin tool call

                # Execute the tool
                from tools.utils.dates import now_iso
                tool_result = self._execute_tool(
                    tool_call_data["use_tool"],
                    tool_call_data.get("args", {}),
                )

                tc = ToolCall(
                    tool_name=tool_call_data["use_tool"],
                    args=tool_call_data.get("args", {}),
                    result=tool_result,
                    timestamp=now_iso(),
                    duration_ms=0,
                )
                tool_calls.append(tc)

                if not tool_result.success:
                    enhanced_input = (
                        f"{enhanced_input}\n\n"
                        f"La herramienta '{tc.tool_name}' falló: "
                        f"{tool_result.error}\nIntenta sin herramientas."
                    )
                else:
                    enhanced_input = (
                        f"{current_input}\n\n"
                        f"Resultado de {tc.tool_name}:\n"
                        f"{tool_result.output}\n\n"
                        f"Ahora responde basándote en esta información."
                    )

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
                tool_calls=tool_calls,
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
                tool_calls=tool_calls,
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

    def _hook_post_run(
        self, run_id: str, result: AgentResult, managed_by_group: bool = False
    ):
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
            # Save tool call outputs as observations
            for tc in result.tool_calls:
                if tc.result.output:
                    content = f"[{tc.tool_name}] {tc.result.output[:300]}"
                    self.db.save_observation(run_id, step_id, content, obs_type="tool_call")
            self.db.complete_run(
                run_id,
                result.output,
                result.duration_ms,
                result.success,
                result.error,
            )
