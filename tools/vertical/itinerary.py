from pathlib import Path

from tools.base import BaseTool, ToolResult, tool

_ACTIVITIES = {
    "cultural": {
        "mañana": ["Visita a museo histórico", "Recorrido por el centro histórico", "Visita a sitios arqueológicos"],
        "tarde": ["Tour de arte y galería", "Visita a mercado de artesanías", "Paseo por barrios coloniales"],
        "noche": ["Cena en restaurante típico", "Espectáculo de danza folclórica", "Recorrido nocturno histórico"],
    },
    "aventura": {
        "mañana": ["Senderismo / hiking", "Ciclismo de montaña", "Escalada"],
        "tarde": ["Rappel", "Kayak / rafting", "Tirolesa"],
        "noche": ["Campamento", "Observación de estrellas", "Fogata y gastronomía local"],
    },
    "relax": {
        "mañana": ["Spa y masajes", "Yoga al amanecer", "Desayuno gourmet en hotel"],
        "tarde": ["Playa o alberca", "Lectura y descanso", "Terapia de flotación"],
        "noche": ["Cena romántica", "Meditación nocturna", "Jacuzzi bajo las estrellas"],
    },
    "gastronómico": {
        "mañana": ["Mercado gourmet local", "Clase de cocina regional", "Degustación de café artesanal"],
        "tarde": ["Tour de bodegas / destilerías", "Visita a productores locales", "Taller de chocolatería"],
        "noche": ["Cena en restaurante de chef reconocido", "Maridaje de vinos", "Cantina tradicional"],
    },
}

_BUDGET_COSTS = {
    "económico": {"daily": 800, "accommodation": 400, "food": 250, "activities": 150},
    "medio": {"daily": 2500, "accommodation": 1400, "food": 700, "activities": 400},
    "premium": {"daily": 8000, "accommodation": 5000, "food": 1800, "activities": 1200},
}


@tool
class ItineraryTool(BaseTool):
    name = "itinerary"
    description = (
        "Genera itinerarios de viaje y turismo. "
        "Úsala para crear planes de viaje detallados, "
        "consultar clima y generar documentos de itinerario."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "generate":
            return self._generate(**kwargs)
        if action == "get_weather":
            return self._get_weather(**kwargs)
        if action == "format_pdf":
            return self._format_pdf(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _generate(
        self,
        destination: str = "",
        days: int = 3,
        travel_style: str = "cultural",
        budget: str = "medio",
    ) -> ToolResult:
        style_acts = _ACTIVITIES.get(travel_style, _ACTIVITIES["cultural"])
        costs = _BUDGET_COSTS.get(budget, _BUDGET_COSTS["medio"])

        lines = [
            f"ITINERARIO — {destination.upper()}",
            f"Duración: {days} días | Estilo: {travel_style} | Presupuesto: {budget}",
            f"Presupuesto estimado total: ${costs['daily'] * days:,.0f} MXN",
            "",
        ]

        import itertools

        mañanas = itertools.cycle(style_acts["mañana"])
        tardes = itertools.cycle(style_acts["tarde"])
        noches = itertools.cycle(style_acts["noche"])

        for day in range(1, days + 1):
            lines.append(f"── DÍA {day} ──")
            lines.append(f"  🌅 Mañana: {next(mañanas)} (${costs['activities']:,.0f})")
            lines.append(f"  ☀ Tarde: {next(tardes)} (${costs['food']:,.0f})")
            lines.append(f"  🌙 Noche: {next(noches)}")
            lines.append(f"  🏨 Hospedaje: ${costs['accommodation']:,.0f}/noche")
            lines.append("")

        lines.append("💡 Tip: Reserva con anticipación para mejores tarifas.")

        return self._success(
            "\n".join(lines),
            raw_data={
                "destination": destination,
                "days": days,
                "style": travel_style,
                "budget": budget,
                "total_estimated": costs["daily"] * days,
            },
        )

    def _get_weather(self, destination: str = "", date: str = None) -> ToolResult:
        api_key = self.credentials.get("openweather_api_key")
        if not api_key:
            return self._success(
                f"Clima no disponible sin API key de OpenWeather. "
                f"Consulta weather.com para {destination}",
                raw_data={"destination": destination},
            )
        import httpx

        try:
            r = httpx.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": destination, "appid": api_key, "units": "metric", "lang": "es"},
                timeout=10,
            )
            r.raise_for_status()
            data = r.json()
            temp = data["main"]["temp"]
            condition = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            return self._success(
                f"Clima en {destination}: {condition}, {temp}°C, humedad {humidity}%",
                raw_data=data,
            )
        except Exception as e:
            return self._error(f"Error al consultar clima: {e}")

    def _format_pdf(
        self,
        itinerary_text: str = "",
        destination: str = "",
        output_path: str = None,
    ) -> ToolResult:
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        except ImportError:
            return self._success(itinerary_text, raw_data={"destination": destination})

        if output_path is None:
            safe = destination[:20].replace(" ", "_")
            output_path = f"data/itineraries/{safe}.pdf"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=inch, bottomMargin=inch)
        styles = getSampleStyleSheet()
        story = [Paragraph(f"ITINERARIO: {destination.upper()}", styles["Heading1"]),
                 Spacer(1, 0.2 * inch)]
        for line in itinerary_text.split("\n"):
            if line.strip():
                story.append(Paragraph(line, styles["Normal"]))
                story.append(Spacer(1, 0.05 * inch))
        try:
            doc.build(story)
            return self._success(
                f"Itinerario PDF generado: {output_path}",
                raw_data={"path": output_path},
            )
        except Exception as e:
            return self._error(f"Error al generar PDF: {e}")
