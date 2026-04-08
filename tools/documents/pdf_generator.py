from datetime import datetime
from pathlib import Path

from tools.base import BaseTool, ToolResult, tool


@tool
class PDFGeneratorTool(BaseTool):
    name = "pdf_generator"
    description = (
        "Genera documentos PDF profesionales. "
        "Úsala para crear cotizaciones, contratos, "
        "reportes o cualquier documento formal."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "generate":
            return self._generate(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _generate(
        self,
        title: str = "",
        content: str = "",
        output_path: str = None,
        company_name: str = "",
    ) -> ToolResult:
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from reportlab.platypus import (
                SimpleDocTemplate,
                Paragraph,
                Spacer,
                HRFlowable,
            )
        except ImportError:
            return self._error(
                "reportlab no instalado. Ejecuta: pip install reportlab"
            )

        if output_path is None:
            safe_title = title[:30].replace(" ", "_")
            output_path = f"data/docs/{safe_title}.pdf"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch,
        )

        styles = getSampleStyleSheet()
        story = []

        # Header
        if company_name:
            story.append(Paragraph(company_name, styles["Heading1"]))
            story.append(Spacer(1, 0.1 * inch))

        story.append(Paragraph(title, styles["Heading2"]))
        story.append(Spacer(1, 0.1 * inch))

        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        story.append(Paragraph(f"Generado: {date_str}", styles["Italic"]))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        story.append(Spacer(1, 0.2 * inch))

        # Content — split by double newline into paragraphs
        for para in content.split("\n\n"):
            para = para.strip()
            if para:
                story.append(Paragraph(para.replace("\n", "<br/>"), styles["Normal"]))
                story.append(Spacer(1, 0.15 * inch))

        try:
            doc.build(story)
        except Exception as e:
            return self._error(f"Error al generar PDF: {e}")

        return self._success(
            f"PDF generado: {output_path}",
            raw_data={"path": output_path},
        )
