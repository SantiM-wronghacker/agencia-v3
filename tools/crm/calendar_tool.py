from tools.base import BaseTool, ToolResult, tool
from tools.utils.http import HTTPClient

_BASE = "https://www.googleapis.com/calendar/v3"


@tool
class GoogleCalendarTool(BaseTool):
    name = "google_calendar"
    description = (
        "Crea y consulta eventos en Google Calendar. "
        "Úsala para agendar citas, reuniones y recordatorios."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "create_event":
            return self._create_event(**kwargs)
        if action == "get_availability":
            return self._get_availability(**kwargs)
        if action == "list_events":
            return self._list_events(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _check_credentials(self) -> ToolResult | None:
        if not self.credentials.get("service_account_json"):
            return self._error("Credencial service_account_json no configurada")
        if not self.credentials.get("calendar_id"):
            return self._error("Credencial calendar_id no configurada")
        return None

    def _get_headers(self) -> dict | None:
        try:
            from google.oauth2 import service_account
            from google.auth.transport.requests import Request

            creds = service_account.Credentials.from_service_account_file(
                self.credentials["service_account_json"],
                scopes=["https://www.googleapis.com/auth/calendar"],
            )
            creds.refresh(Request())
            return {
                "Authorization": f"Bearer {creds.token}",
                "Content-Type": "application/json",
            }
        except ImportError:
            return None
        except Exception:
            return None

    def _create_event(
        self,
        title: str = "",
        start: str = "",
        end: str = "",
        attendees: list = None,
        description: str = "",
    ) -> ToolResult:
        err = self._check_credentials()
        if err:
            return err

        headers = self._get_headers()
        if headers is None:
            return self._error(
                "google-auth no instalado o credenciales inválidas. "
                "Ejecuta: pip install google-auth"
            )

        calendar_id = self.credentials["calendar_id"]
        body = {
            "summary": title,
            "description": description,
            "start": {"dateTime": start, "timeZone": "America/Mexico_City"},
            "end": {"dateTime": end, "timeZone": "America/Mexico_City"},
            "attendees": [{"email": e} for e in (attendees or [])],
        }

        client = HTTPClient(_BASE, headers=headers)
        resp = client.post(f"/calendars/{calendar_id}/events", json=body)
        if not resp or "id" not in resp:
            return self._error(f"Error al crear evento en Google Calendar")

        event_id = resp["id"]
        return self._success(
            f"Evento '{title}' creado",
            raw_data={"event_id": event_id},
        )

    def _get_availability(
        self, date: str = "", duration_minutes: int = 60
    ) -> ToolResult:
        err = self._check_credentials()
        if err:
            return err

        headers = self._get_headers()
        if headers is None:
            return self._error(
                "google-auth no instalado o credenciales inválidas. "
                "Ejecuta: pip install google-auth"
            )

        calendar_id = self.credentials["calendar_id"]
        client = HTTPClient(_BASE, headers=headers)
        resp = client.get(
            f"/calendars/{calendar_id}/events",
            params={
                "timeMin": f"{date}T00:00:00Z",
                "timeMax": f"{date}T23:59:59Z",
                "orderBy": "startTime",
                "singleEvents": "true",
            },
        )
        if not resp:
            return self._error("Error al consultar disponibilidad en Google Calendar")

        events = resp.get("items", [])
        busy_slots = []
        for ev in events:
            start = ev.get("start", {}).get("dateTime", "")
            end = ev.get("end", {}).get("dateTime", "")
            if start and end:
                busy_slots.append(f"  Ocupado: {start[11:16]} - {end[11:16]}")

        lines = [f"Disponibilidad para {date}:"]
        if busy_slots:
            lines.append(f"  Eventos ({len(busy_slots)}): ")
            lines.extend(busy_slots)
        else:
            lines.append("  Día libre — sin eventos registrados")

        return self._success("\n".join(lines), raw_data={"events": events})

    def _list_events(self, date_from: str = "", date_to: str = "") -> ToolResult:
        err = self._check_credentials()
        if err:
            return err

        headers = self._get_headers()
        if headers is None:
            return self._error(
                "google-auth no instalado o credenciales inválidas. "
                "Ejecuta: pip install google-auth"
            )

        calendar_id = self.credentials["calendar_id"]
        client = HTTPClient(_BASE, headers=headers)
        resp = client.get(
            f"/calendars/{calendar_id}/events",
            params={
                "timeMin": f"{date_from}T00:00:00Z",
                "timeMax": f"{date_to}T23:59:59Z",
                "orderBy": "startTime",
                "singleEvents": "true",
            },
        )
        if not resp:
            return self._error("Error al listar eventos de Google Calendar")

        events = resp.get("items", [])
        lines = [f"Eventos del {date_from} al {date_to} ({len(events)}):"]
        for ev in events:
            title = ev.get("summary", "Sin título")
            start = ev.get("start", {}).get("dateTime", ev.get("start", {}).get("date", ""))
            lines.append(f"  - {title} ({start[:16]})")

        return self._success("\n".join(lines), raw_data={"events": events})
