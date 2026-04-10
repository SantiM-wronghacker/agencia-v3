from tools.base import BaseTool, ToolResult, tool

_BASE = "https://www.banxico.org.mx/SieAPIRest/service/v1/series"

_SERIES = {
    "inflation": "SP30578",
    "interest_rate": "SF43783",
    "exchange_rate": "SF43718",
    "tiie_28": "SF44096",
}

_LABELS = {
    "inflation": "Inflación anual (INPC)",
    "interest_rate": "Tasa objetivo Banxico",
    "exchange_rate": "Tipo de cambio USD/MXN",
    "tiie_28": "TIIE 28 días",
}


@tool
class BanxicoTool(BaseTool):
    name = "banxico"
    description = (
        "Consulta datos oficiales del Banco de México. "
        "Úsala para obtener inflación, tasas de interés "
        "y tipo de cambio oficial."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "get_inflation":
            return self._get_series("inflation")
        if action == "get_interest_rate":
            return self._get_series("interest_rate")
        if action == "get_exchange_rate":
            return self._get_series("exchange_rate")
        if action == "get_tiie":
            return self._get_series("tiie_28")
        if action == "get_all":
            return self._get_all()
        return self._error(f"Acción '{action}' no soportada")

    def _get_series(self, series_name: str) -> ToolResult:
        series_id = _SERIES[series_name]
        token = self.credentials.get("banxico_token", "DEMO_TOKEN")
        import httpx

        try:
            r = httpx.get(
                f"{_BASE}/{series_id}/datos/oportuno",
                headers={"Bmx-Token": token, "Accept": "application/json"},
                timeout=10,
            )
            if r.status_code == 401:
                return self._success(
                    f"{series_name}: datos no disponibles sin token BANXICO.\n"
                    f"Regístrate en https://www.banxico.org.mx/SieAPIRest/ "
                    f"para obtener tu token gratuito.",
                    raw_data={"series": series_name, "requires_token": True},
                )
            r.raise_for_status()
            data = r.json()
            series = data.get("bmx", {}).get("series", [{}])[0]
            datos = series.get("datos", [{}])
            ultimo = datos[-1] if datos else {}
            valor = ultimo.get("dato", "N/D")
            fecha = ultimo.get("fecha", "")
            label = _LABELS.get(series_name, series_name)
            return self._success(
                f"{label}: {valor}% ({fecha})",
                raw_data={"value": valor, "date": fecha, "series": series_name},
            )
        except Exception as e:
            return self._error(f"Error consultando BANXICO: {e}")

    def _get_all(self) -> ToolResult:
        lines = ["=== INDICADORES BANXICO ==="]
        all_data = {}
        for series_name in _SERIES:
            result = self._get_series(series_name)
            lines.append(result.output if result.success else f"{series_name}: {result.error}")
            if result.raw_data:
                all_data[series_name] = result.raw_data
        return self._success("\n".join(lines), raw_data=all_data)
