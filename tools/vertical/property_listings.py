import json
from pathlib import Path
from uuid import uuid4

from tools.base import BaseTool, ToolResult, tool
from tools.utils.dates import now_iso

_DATA_FILE = Path("data/properties.json")


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
class PropertyListingsTool(BaseTool):
    name = "property_listings"
    description = (
        "Gestiona listados de propiedades inmobiliarias. "
        "Úsala para crear fichas, actualizar precios "
        "y generar reportes de propiedades."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "create":
            return self._create(**kwargs)
        if action == "update":
            return self._update(**kwargs)
        if action == "list":
            return self._list(**kwargs)
        if action == "generate_report":
            return self._generate_report(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _create(
        self,
        title: str = "",
        property_type: str = "casa",
        operation: str = "venta",
        price: float = 0.0,
        location: str = "",
        bedrooms: int = 0,
        bathrooms: int = 0,
        area_m2: float = 0.0,
        description: str = "",
    ) -> ToolResult:
        prop_id = str(uuid4())[:8].upper()
        property_dict = {
            "id": prop_id,
            "title": title,
            "property_type": property_type,
            "operation": operation,
            "price": price,
            "location": location,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "area_m2": area_m2,
            "description": description,
            "status": "active",
            "created_at": now_iso(),
        }
        data = _load()
        data.append(property_dict)
        _save(data)
        return self._success(
            f"Propiedad '{title}' registrada. "
            f"ID: {prop_id}. {operation.title()}: ${price:,.0f}",
            raw_data=property_dict,
        )

    def _update(self, property_id: str = "", **fields) -> ToolResult:
        data = _load()
        for prop in data:
            if prop.get("id") == property_id:
                for k, v in fields.items():
                    if k != "property_id":
                        prop[k] = v
                _save(data)
                return self._success(f"Propiedad {property_id} actualizada")
        return self._error(f"Propiedad '{property_id}' no encontrada")

    def _list(
        self,
        operation: str = None,
        property_type: str = None,
        max_price: float = None,
    ) -> ToolResult:
        data = _load()
        results = [p for p in data if p.get("status") == "active"]
        if operation:
            results = [p for p in results if p.get("operation") == operation]
        if property_type:
            results = [p for p in results if p.get("property_type") == property_type]
        if max_price is not None:
            results = [p for p in results if p.get("price", 0) <= max_price]
        if not results:
            return self._success("Sin propiedades para los filtros especificados")
        lines = [f"Propiedades ({len(results)}):"]
        for p in results:
            lines.append(
                f"  [{p['id']}] {p['title']} — {p['operation'].title()}: ${p['price']:,.0f} "
                f"| {p['location']} | {p.get('bedrooms',0)}rec {p.get('bathrooms',0)}baños "
                f"{p.get('area_m2',0)}m²"
            )
        return self._success("\n".join(lines), raw_data={"properties": results})

    def _generate_report(
        self,
        property_id: str = "",
        output_path: str = None,
    ) -> ToolResult:
        data = _load()
        prop = next((p for p in data if p.get("id") == property_id), None)
        if not prop:
            return self._error(f"Propiedad '{property_id}' no encontrada")

        text_report = (
            f"FICHA DE PROPIEDAD\n"
            f"==================\n"
            f"ID: {prop['id']}\n"
            f"Título: {prop['title']}\n"
            f"Tipo: {prop['property_type']}\n"
            f"Operación: {prop['operation']}\n"
            f"Precio: ${prop['price']:,.0f}\n"
            f"Ubicación: {prop['location']}\n"
            f"Recámaras: {prop.get('bedrooms', 0)}\n"
            f"Baños: {prop.get('bathrooms', 0)}\n"
            f"Área: {prop.get('area_m2', 0)} m²\n"
            f"Descripción: {prop.get('description', '')}\n"
        )

        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

            if output_path is None:
                output_path = f"data/reports/property_{property_id}.pdf"
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            doc = SimpleDocTemplate(output_path, pagesize=letter,
                                    rightMargin=inch, leftMargin=inch,
                                    topMargin=inch, bottomMargin=inch)
            styles = getSampleStyleSheet()
            story = [
                Paragraph("FICHA DE PROPIEDAD", styles["Heading1"]),
                Spacer(1, 0.2 * inch),
            ]
            for line in text_report.split("\n")[3:]:
                if line.strip():
                    story.append(Paragraph(line, styles["Normal"]))
                    story.append(Spacer(1, 0.1 * inch))
            doc.build(story)
            return self._success(
                f"Reporte generado: {output_path}",
                raw_data={"path": output_path, "property": prop},
            )
        except ImportError:
            return self._success(text_report, raw_data={"property": prop})
        except Exception as e:
            return self._error(f"Error al generar reporte: {e}")
