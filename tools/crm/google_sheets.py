from tools.base import BaseTool, ToolResult, tool
from tools.utils.http import HTTPClient

_BASE = "https://sheets.googleapis.com/v4/spreadsheets"


@tool
class GoogleSheetsTool(BaseTool):
    name = "google_sheets"
    description = (
        "Lee y escribe datos en Google Sheets. "
        "Úsala como CRM simple o para leer/guardar datos "
        "de clientes en hojas de cálculo."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "read":
            return self._read(**kwargs)
        if action == "append_row":
            return self._append_row(**kwargs)
        if action == "update_cell":
            return self._update_cell(**kwargs)
        if action == "find_row":
            return self._find_row(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _check_credentials(self) -> ToolResult | None:
        if not self.credentials.get("service_account_json"):
            return self._error("Credencial service_account_json no configurada")
        if not self.credentials.get("spreadsheet_id"):
            return self._error("Credencial spreadsheet_id no configurada")
        return None

    def _get_headers(self) -> dict | None:
        try:
            import json
            from google.oauth2 import service_account
            from google.auth.transport.requests import Request

            creds = service_account.Credentials.from_service_account_file(
                self.credentials["service_account_json"],
                scopes=["https://www.googleapis.com/auth/spreadsheets"],
            )
            creds.refresh(Request())
            return {"Authorization": f"Bearer {creds.token}"}
        except ImportError:
            return None
        except Exception:
            return None

    def _read(self, range: str = "Sheet1!A1:Z100") -> ToolResult:
        err = self._check_credentials()
        if err:
            return err

        headers = self._get_headers()
        if headers is None:
            return self._error(
                "google-auth no instalado o credenciales inválidas. "
                "Ejecuta: pip install google-auth"
            )

        spreadsheet_id = self.credentials["spreadsheet_id"]
        client = HTTPClient(_BASE, headers=headers)
        resp = client.get(f"/{spreadsheet_id}/values/{range}")
        if not resp:
            return self._error("Error al leer Google Sheets")

        rows = resp.get("values", [])
        if not rows:
            return self._success("Hoja vacía")

        lines = []
        for row in rows:
            lines.append(" | ".join(str(cell) for cell in row))
        return self._success("\n".join(lines), raw_data={"rows": rows})

    def _append_row(
        self, values: list = None, range: str = "Sheet1!A:A"
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

        spreadsheet_id = self.credentials["spreadsheet_id"]
        headers["Content-Type"] = "application/json"
        client = HTTPClient(_BASE, headers=headers)
        resp = client.post(
            f"/{spreadsheet_id}/values/{range}:append",
            json={"values": [values or []], "valueInputOption": "USER_ENTERED"},
        )
        if not resp:
            return self._error("Error al agregar fila en Google Sheets")

        return self._success(f"Fila agregada: {values}", raw_data=resp)

    def _update_cell(self, cell: str = "", value: str = "") -> ToolResult:
        err = self._check_credentials()
        if err:
            return err

        headers = self._get_headers()
        if headers is None:
            return self._error(
                "google-auth no instalado o credenciales inválidas. "
                "Ejecuta: pip install google-auth"
            )

        spreadsheet_id = self.credentials["spreadsheet_id"]
        headers["Content-Type"] = "application/json"
        client = HTTPClient(_BASE, headers=headers)
        resp = client.post(
            f"/{spreadsheet_id}/values/{cell}",
            json={"values": [[value]], "valueInputOption": "USER_ENTERED"},
        )
        if not resp:
            return self._error(f"Error al actualizar celda {cell} en Google Sheets")

        return self._success(
            f"Celda {cell} actualizada a '{value}'",
            raw_data={"cell": cell, "value": value},
        )

    def _find_row(
        self, column_values: list = None, search_value: str = ""
    ) -> ToolResult:
        column_values = column_values or []
        for i, val in enumerate(column_values):
            if str(val) == str(search_value):
                return self._success(
                    f"'{search_value}' encontrado en fila {i + 1}",
                    raw_data={"row_index": i, "value": val},
                )
        return self._error(f"'{search_value}' no encontrado")
