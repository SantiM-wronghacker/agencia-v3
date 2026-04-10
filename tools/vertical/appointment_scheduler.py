import json
from pathlib import Path
from uuid import uuid4

from tools.base import BaseTool, ToolResult, tool
from tools.utils.dates import now_iso

_DATA_FILE = Path("data/appointments.json")


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
class AppointmentSchedulerTool(BaseTool):
    name = "appointment_scheduler"
    description = (
        "Gestiona citas para clínicas y consultorios. "
        "Úsala para crear, consultar y recordar citas médicas."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "create":
            return self._create(**kwargs)
        if action == "list":
            return self._list(**kwargs)
        if action == "cancel":
            return self._cancel(**kwargs)
        if action == "send_reminder":
            return self._send_reminder(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _create(
        self,
        patient_name: str = "",
        doctor: str = "",
        date: str = "",
        time: str = "",
        appointment_type: str = "consulta",
        phone: str = "",
    ) -> ToolResult:
        appointment = {
            "id": str(uuid4())[:8].upper(),
            "patient_name": patient_name,
            "doctor": doctor,
            "date": date,
            "time": time,
            "appointment_type": appointment_type,
            "phone": phone,
            "status": "scheduled",
            "created_at": now_iso(),
        }
        data = _load()
        data.append(appointment)
        _save(data)
        return self._success(
            f"Cita creada: {patient_name} con Dr. {doctor} "
            f"el {date} a las {time}. Tipo: {appointment_type}",
            raw_data=appointment,
        )

    def _list(self, date: str = None, doctor: str = None) -> ToolResult:
        data = _load()
        results = [a for a in data if a.get("status") != "cancelled"]
        if date:
            results = [a for a in results if a.get("date") == date]
        if doctor:
            results = [
                a for a in results if doctor.lower() in a.get("doctor", "").lower()
            ]
        results = sorted(results, key=lambda a: (a.get("date", ""), a.get("time", "")))
        if not results:
            return self._success("Sin citas para los filtros especificados")
        lines = ["Agenda:"]
        for a in results:
            lines.append(
                f"  [{a['id']}] {a['date']} {a['time']} — {a['patient_name']} "
                f"con Dr. {a['doctor']} ({a['appointment_type']})"
            )
        return self._success("\n".join(lines), raw_data={"appointments": results})

    def _cancel(self, appointment_id: str = "", reason: str = "") -> ToolResult:
        data = _load()
        for a in data:
            if a.get("id") == appointment_id:
                a["status"] = "cancelled"
                if reason:
                    a["cancel_reason"] = reason
                _save(data)
                return self._success(f"Cita {appointment_id} cancelada")
        return self._error(f"Cita '{appointment_id}' no encontrada")

    def _send_reminder(self, appointment_id: str = "") -> ToolResult:
        data = _load()
        appointment = next((a for a in data if a.get("id") == appointment_id), None)
        if not appointment:
            return self._error(f"Cita '{appointment_id}' no encontrada")

        reminder_text = (
            f"Recordatorio de cita:\n"
            f"Paciente: {appointment['patient_name']}\n"
            f"Doctor: Dr. {appointment['doctor']}\n"
            f"Fecha: {appointment['date']} a las {appointment['time']}\n"
            f"Tipo: {appointment['appointment_type']}"
        )

        wa_token = self.credentials.get("whatsapp_token")
        wa_phone_id = self.credentials.get("whatsapp_phone_id")
        patient_phone = appointment.get("phone", "")

        if wa_token and wa_phone_id and patient_phone:
            try:
                import httpx

                httpx.post(
                    f"https://graph.facebook.com/v18.0/{wa_phone_id}/messages",
                    json={
                        "messaging_product": "whatsapp",
                        "to": patient_phone,
                        "type": "text",
                        "text": {"body": reminder_text},
                    },
                    headers={"Authorization": f"Bearer {wa_token}"},
                    timeout=10,
                )
                return self._success(
                    f"Recordatorio enviado por WhatsApp a {patient_phone}",
                    raw_data={"reminder": reminder_text},
                )
            except Exception as e:
                return self._error(f"Error al enviar recordatorio: {e}")

        return self._success(
            f"Recordatorio listo para enviar manualmente:\n\n{reminder_text}",
            raw_data={"reminder": reminder_text},
        )
