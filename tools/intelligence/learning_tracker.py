import json
from pathlib import Path

from tools.base import BaseTool, ToolResult, tool
from tools.utils.dates import now_iso

_DATA_FILE = Path("data/learning_progress.json")


def _load() -> list:
    if not _DATA_FILE.exists():
        return []
    try:
        return json.loads(_DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save(data: list) -> None:
    _DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    _DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


@tool
class LearningTrackerTool(BaseTool):
    name = "learning_tracker"
    description = (
        "Rastrea el progreso de aprendizaje de estudiantes. "
        "Úsala para registrar avances, generar reportes "
        "e identificar áreas de mejora."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "record_progress":
            return self._record_progress(**kwargs)
        if action == "get_report":
            return self._get_report(**kwargs)
        if action == "identify_weak":
            return self._identify_weak(**kwargs)
        if action == "list_students":
            return self._list_students()
        return self._error(f"Acción '{action}' no soportada")

    def _record_progress(
        self,
        student_id: str = "",
        module: str = "",
        score: float = 0.0,
        time_spent_min: int = 0,
    ) -> ToolResult:
        if not student_id:
            return self._error("El parámetro 'student_id' es obligatorio")
        if not module:
            return self._error("El parámetro 'module' es obligatorio")
        data = _load()
        data.append({
            "student_id": student_id,
            "module": module,
            "score": score,
            "time_spent_min": time_spent_min,
            "timestamp": now_iso(),
        })
        _save(data)
        return self._success(
            f"Progreso registrado: {student_id} — {module}: {score:.0f}%",
            raw_data={"student_id": student_id, "module": module, "score": score},
        )

    def _get_report(self, student_id: str = "") -> ToolResult:
        data = _load()
        records = [r for r in data if r.get("student_id") == student_id]
        if not records:
            return self._error(f"Sin registros para estudiante '{student_id}'")
        scores = [r["score"] for r in records]
        avg = sum(scores) / len(scores)
        total_time = sum(r.get("time_spent_min", 0) for r in records)
        modules = list({r["module"] for r in records})
        weak = [r["module"] for r in records if r["score"] < 70]
        lines = [
            f"=== REPORTE: {student_id} ===",
            f"Promedio general: {avg:.1f}%",
            f"Módulos cursados: {len(modules)}",
            f"Tiempo total: {total_time} minutos",
            f"Módulos aprobados: {sum(1 for s in scores if s >= 70)}/{len(scores)}",
        ]
        if weak:
            lines.append(f"Módulos con score < 70%: {', '.join(set(weak))}")
        return self._success(
            "\n".join(lines),
            raw_data={"student_id": student_id, "avg": avg, "modules": modules,
                      "total_time_min": total_time},
        )

    def _identify_weak(self, student_id: str = "", threshold: float = 70.0) -> ToolResult:
        data = _load()
        records = [r for r in data if r.get("student_id") == student_id]
        if not records:
            return self._error(f"Sin registros para estudiante '{student_id}'")
        weak = [(r["module"], r["score"]) for r in records if r["score"] < threshold]
        if not weak:
            return self._success(
                f"Sin áreas débiles para {student_id} (umbral: {threshold}%)"
            )
        lines = [f"Áreas de mejora para {student_id} (score < {threshold}%):"]
        for module, score in weak:
            lines.append(f"  ⚠ {module}: {score:.0f}%")
        return self._success(
            "\n".join(lines),
            raw_data={"student_id": student_id, "weak_modules": weak},
        )

    def _list_students(self) -> ToolResult:
        data = _load()
        if not data:
            return self._success("Sin estudiantes registrados")
        from collections import defaultdict
        students: dict = defaultdict(list)
        for r in data:
            students[r["student_id"]].append(r["score"])
        lines = ["Estudiantes registrados:"]
        for sid, scores in sorted(students.items()):
            avg = sum(scores) / len(scores)
            lines.append(f"  {sid}: promedio {avg:.1f}% ({len(scores)} registros)")
        return self._success("\n".join(lines),
                             raw_data={"students": list(students.keys())})
