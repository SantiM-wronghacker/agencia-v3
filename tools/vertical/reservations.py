import json
from pathlib import Path
from uuid import uuid4

from tools.base import BaseTool, ToolResult, tool
from tools.utils.dates import now_iso

_DATA_FILE = Path("data/reservations.json")
_DEFAULT_CAPACITY = 50


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
class ReservationsTool(BaseTool):
    name = "reservations"
    description = (
        "Gestiona reservaciones para restaurantes y hospitality. "
        "Úsala para crear, consultar y confirmar reservaciones."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "create":
            return self._create(**kwargs)
        if action == "check_availability":
            return self._check_availability(**kwargs)
        if action == "list_today":
            return self._list_today()
        if action == "confirm":
            return self._confirm(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _create(
        self,
        name: str = "",
        date: str = "",
        time: str = "",
        party_size: int = 1,
        phone: str = "",
        notes: str = "",
    ) -> ToolResult:
        reservation = {
            "id": str(uuid4())[:8].upper(),
            "name": name,
            "date": date,
            "time": time,
            "party_size": party_size,
            "phone": phone,
            "notes": notes,
            "status": "confirmed",
            "created_at": now_iso(),
        }

        sheets_id = self.credentials.get("sheets_id")
        sa_json = self.credentials.get("google_service_account_json")
        if sheets_id and sa_json:
            try:
                import httpx

                httpx.post(
                    f"https://sheets.googleapis.com/v4/spreadsheets/{sheets_id}/values/A1:append",
                    json={"values": [list(reservation.values())]},
                    timeout=10,
                )
            except Exception:
                pass  # Fall through to local save

        data = _load()
        data.append(reservation)
        _save(data)

        return self._success(
            f"Reservación creada: {name} para {party_size} personas "
            f"el {date} a las {time}. ID: {reservation['id']}",
            raw_data=reservation,
        )

    def _check_availability(
        self,
        date: str = "",
        time: str = "",
        party_size: int = 1,
    ) -> ToolResult:
        data = _load()
        capacity = int(self.credentials.get("max_capacity", _DEFAULT_CAPACITY))
        occupied = sum(
            r.get("party_size", 0)
            for r in data
            if r.get("date") == date
            and r.get("time") == time
            and r.get("status") != "cancelled"
        )
        available = capacity - occupied
        hay_espacio = available >= party_size
        return self._success(
            f"{'Disponible' if hay_espacio else 'Sin disponibilidad'} "
            f"para {party_size} personas el {date} a las {time}. "
            f"Lugares disponibles: {max(0, available)}/{capacity}",
            raw_data={"available": hay_espacio, "spots_left": max(0, available)},
        )

    def _list_today(self) -> ToolResult:
        from datetime import date as date_cls

        today = date_cls.today().isoformat()
        data = _load()
        today_reservations = sorted(
            [r for r in data if r.get("date") == today and r.get("status") != "cancelled"],
            key=lambda r: r.get("time", ""),
        )
        if not today_reservations:
            return self._success(f"Sin reservaciones para hoy ({today})")
        lines = [f"Reservaciones para {today}:"]
        for r in today_reservations:
            lines.append(
                f"  {r['time']} - {r['name']} ({r['party_size']} personas) [ID: {r['id']}]"
            )
        return self._success("\n".join(lines), raw_data={"reservations": today_reservations})

    def _confirm(self, reservation_id: str = "") -> ToolResult:
        data = _load()
        for r in data:
            if r.get("id") == reservation_id:
                r["status"] = "confirmed"
                _save(data)
                return self._success(f"Reservación {reservation_id} confirmada")
        return self._error(f"Reservación '{reservation_id}' no encontrada")
