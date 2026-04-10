import re
import uuid
from pathlib import Path

from tools.base import BaseTool, ToolResult, tool
from tools.utils.dates import now_iso

_DATA_FILE = Path("data/scheduled_tasks.json")
_FIELD_RE = re.compile(
    r"^(\*|(\*/\d+)|(\d+(-\d+)?)|((\d+,)+\d+))$"
)


def _validate_field(val: str) -> bool:
    return bool(_FIELD_RE.match(val.strip()))


@tool
class SchedulerTool(BaseTool):
    name = "scheduler"
    description = (
        "Programa tareas automáticas con expresiones cron. "
        "Úsala para ejecutar grupos de agentes "
        "en horarios específicos."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "schedule":
            return self._schedule(**kwargs)
        if action == "list_tasks":
            return self._list_tasks()
        if action == "cancel":
            return self._cancel(**kwargs)
        if action == "validate_cron":
            return self._validate_cron(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    # ------------------------------------------------------------------
    def _load(self) -> list:
        if _DATA_FILE.exists():
            import json
            try:
                return json.loads(_DATA_FILE.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []

    def _save(self, tasks: list) -> None:
        import json
        _DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        _DATA_FILE.write_text(json.dumps(tasks, indent=2, ensure_ascii=False), encoding="utf-8")

    # ------------------------------------------------------------------
    def _schedule(
        self,
        group_name: str = "",
        task: str = "",
        cron_expression: str = "",
        task_id: str = None,
    ) -> ToolResult:
        val = self._validate_cron(cron_expression=cron_expression)
        if not val.success:
            return val
        tid = task_id or str(uuid.uuid4())[:8]
        next_desc = self._describe_cron(cron_expression)
        entry = {
            "id": tid,
            "group_name": group_name,
            "task": task,
            "cron": cron_expression,
            "created_at": now_iso(),
            "active": True,
            "last_run": None,
            "next_description": next_desc,
        }
        tasks = self._load()
        tasks.append(entry)
        self._save(tasks)
        return self._success(
            f"Tarea programada: {group_name} — {cron_expression}\n"
            f"Próxima ejecución: {next_desc}",
            raw_data=entry,
        )

    def _list_tasks(self) -> ToolResult:
        tasks = self._load()
        if not tasks:
            return self._success("No hay tareas programadas.", raw_data={"tasks": []})
        lines = ["ID       | Grupo                | Cron            | Activa | Último run",
                 "-" * 75]
        for t in tasks:
            lines.append(
                f"{t['id'][:8]:<9}| {t['group_name'][:20]:<22}| "
                f"{t['cron']:<17}| {'Sí' if t['active'] else 'No':<7}| "
                f"{t.get('last_run') or 'N/A'}"
            )
        return self._success("\n".join(lines), raw_data={"tasks": tasks})

    def _cancel(self, task_id: str = "") -> ToolResult:
        tasks = self._load()
        found = False
        for t in tasks:
            if t["id"] == task_id:
                t["active"] = False
                found = True
                break
        if not found:
            return self._error(f"Tarea '{task_id}' no encontrada")
        self._save(tasks)
        return self._success(f"Tarea {task_id} cancelada", raw_data={"id": task_id})

    def _validate_cron(self, cron_expression: str = "") -> ToolResult:
        parts = cron_expression.strip().split()
        if len(parts) != 5:
            return self._error(
                f"Cron inválido: '{cron_expression}'\n"
                "Formato: 'min hora día mes día_semana'\n"
                "Ejemplos:\n"
                "  '0 9 * * 1-5' — lun-vie 9am\n"
                "  '0 8 * * 1'   — lunes 8am\n"
                "  '*/30 * * * *'— cada 30 min"
            )
        for p in parts:
            if not _validate_field(p):
                return self._error(
                    f"Cron inválido: '{cron_expression}'\n"
                    "Formato: 'min hora día mes día_semana'\n"
                    "Ejemplos:\n"
                    "  '0 9 * * 1-5' — lun-vie 9am\n"
                    "  '0 8 * * 1'   — lunes 8am\n"
                    "  '*/30 * * * *'— cada 30 min"
                )
        return self._success("Expresión cron válida", raw_data={"cron": cron_expression})

    def _describe_cron(self, cron: str) -> str:
        parts = cron.strip().split()
        if len(parts) != 5:
            return f"Ver expresión: {cron}"
        minute, hour, day, month, dow = parts
        # every N minutes
        m = re.match(r"^\*/(\d+)$", minute)
        if m and hour == "*" and day == "*" and month == "*" and dow == "*":
            return f"Cada {m.group(1)} minutos"
        # specific hour, every day
        if re.match(r"^\d+$", minute) and re.match(r"^\d+$", hour):
            h = int(hour)
            m_val = int(minute)
            ampm = "am" if h < 12 else "pm"
            h12 = h if 1 <= h <= 12 else (h - 12 if h > 12 else 12)
            time_str = f"{h12}:{m_val:02d}{ampm}"
            # mon-fri
            if dow == "1-5" and day == "*" and month == "*":
                return f"Lunes a viernes a las {time_str}"
            # specific day of week
            dow_names = {"1": "Lunes", "2": "Martes", "3": "Miércoles",
                         "4": "Jueves", "5": "Viernes", "6": "Sábado",
                         "0": "Domingo", "7": "Domingo"}
            if re.match(r"^[0-7]$", dow) and day == "*" and month == "*":
                return f"{dow_names.get(dow, dow)} a las {time_str}"
            # first day of month
            if dow == "*" and day == "1" and month == "*":
                return f"Primer día de cada mes a las {time_str}"
            if dow == "*" and day == "*" and month == "*":
                return f"Todos los días a las {time_str}"
        return f"Ver expresión: {cron}"

    def _get_scheduler(self):
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            return BackgroundScheduler
        except ImportError:
            return None
