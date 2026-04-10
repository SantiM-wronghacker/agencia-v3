from pathlib import Path

from tools.base import BaseTool, ToolResult, tool


@tool
class PatientFormsTool(BaseTool):
    name = "patient_forms"
    description = (
        "Genera formularios de paciente en PDF. "
        "Úsala para crear fichas de registro, "
        "consentimientos y formularios de anamnesis."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "generate_intake":
            return self._generate_intake(**kwargs)
        if action == "generate_consent":
            return self._generate_consent(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _generate_intake(
        self,
        patient_name: str = "",
        clinic_name: str = "",
        output_path: str = None,
    ) -> ToolResult:
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
        except ImportError:
            return self._error("reportlab no instalado. Ejecuta: pip install reportlab")

        if output_path is None:
            safe = patient_name[:20].replace(" ", "_")
            output_path = f"data/forms/intake_{safe}.pdf"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=inch, bottomMargin=inch)
        styles = getSampleStyleSheet()
        story = []

        if clinic_name:
            story.append(Paragraph(clinic_name, styles["Heading1"]))
        story.append(Paragraph("FICHA DE REGISTRO DE PACIENTE", styles["Heading2"]))
        story.append(Spacer(1, 0.1 * inch))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        story.append(Spacer(1, 0.2 * inch))

        fields = [
            ("Paciente", patient_name),
            ("Fecha de nacimiento", "________________"),
            ("Sexo", "________________"),
            ("Teléfono", "________________"),
            ("Correo electrónico", "________________"),
            ("Dirección", "________________"),
        ]
        for label, value in fields:
            story.append(Paragraph(f"<b>{label}:</b> {value}", styles["Normal"]))
            story.append(Spacer(1, 0.1 * inch))

        story.append(Paragraph("<b>ANTECEDENTES MÉDICOS</b>", styles["Heading3"]))
        for section in ["Enfermedades crónicas", "Cirugías previas", "Alergias conocidas",
                         "Medicamentos actuales", "Motivo de consulta"]:
            story.append(Paragraph(f"{section}:", styles["Normal"]))
            story.append(Paragraph("________________" * 4, styles["Normal"]))
            story.append(Spacer(1, 0.15 * inch))

        try:
            doc.build(story)
        except Exception as e:
            return self._error(f"Error al generar formulario: {e}")

        return self._success(
            f"Formulario de ingreso generado: {output_path}",
            raw_data={"path": output_path},
        )

    def _generate_consent(
        self,
        patient_name: str = "",
        procedure: str = "",
        doctor_name: str = "",
        clinic_name: str = "",
        output_path: str = None,
    ) -> ToolResult:
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
        except ImportError:
            return self._error("reportlab no instalado. Ejecuta: pip install reportlab")

        if output_path is None:
            safe = patient_name[:20].replace(" ", "_")
            output_path = f"data/forms/consent_{safe}.pdf"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=inch, bottomMargin=inch)
        styles = getSampleStyleSheet()
        story = []

        if clinic_name:
            story.append(Paragraph(clinic_name, styles["Heading1"]))
        story.append(Paragraph("CONSENTIMIENTO INFORMADO", styles["Heading2"]))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph(f"<b>Paciente:</b> {patient_name}", styles["Normal"]))
        story.append(Paragraph(f"<b>Procedimiento:</b> {procedure}", styles["Normal"]))
        if doctor_name:
            story.append(Paragraph(f"<b>Médico responsable:</b> Dr. {doctor_name}", styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))

        body = (
            f"Yo, {patient_name}, declaro haber sido informado/a sobre el procedimiento "
            f"'{procedure}', incluyendo sus riesgos, beneficios y alternativas de tratamiento. "
            "Comprendo la información recibida y doy mi consentimiento para su realización."
        )
        story.append(Paragraph(body, styles["Normal"]))
        story.append(Spacer(1, 0.3 * inch))

        for label in ["Riesgos", "Beneficios esperados", "Alternativas de tratamiento"]:
            story.append(Paragraph(f"<b>{label}:</b>", styles["Normal"]))
            story.append(Paragraph("________________" * 4, styles["Normal"]))
            story.append(Spacer(1, 0.15 * inch))

        story.append(Spacer(1, 0.4 * inch))
        story.append(Paragraph("Firma del paciente: ____________________________  "
                               "Fecha: ______________", styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("Firma del médico: ______________________________  "
                               "Cédula: ______________", styles["Normal"]))

        try:
            doc.build(story)
        except Exception as e:
            return self._error(f"Error al generar consentimiento: {e}")

        return self._success(
            f"Consentimiento informado generado: {output_path}",
            raw_data={"path": output_path},
        )
