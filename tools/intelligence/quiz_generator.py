import json
from pathlib import Path
from uuid import uuid4

from tools.base import BaseTool, ToolResult, tool
from tools.utils.dates import now_iso

_DATA_DIR = Path("data/quizzes")

_QUESTION_TEMPLATES = {
    "easy": [
        ("¿Cuál es el concepto básico de {topic}?",
         ["Definición A", "Definición B", "Definición C", "Definición D"], "a",
         "Esta es la definición fundamental."),
        ("¿Qué característica principal tiene {topic}?",
         ["Característica 1", "Característica 2", "Característica 3", "Característica 4"], "b",
         "Esta característica es clave en el campo."),
    ],
    "medium": [
        ("En el contexto de {topic}, ¿cuál es el enfoque más apropiado?",
         ["Enfoque analítico", "Enfoque práctico", "Enfoque teórico", "Ninguno"], "b",
         "El enfoque práctico es el más efectivo en este caso."),
        ("¿Cómo se aplica {topic} en un caso real?",
         ["Opción A", "Opción B", "Opción C", "Opción D"], "a",
         "La aplicación correcta sigue este principio."),
    ],
    "hard": [
        ("Analiza la implicación avanzada de {topic} en sistemas complejos:",
         ["Implicación 1", "Implicación 2", "Implicación 3", "Implicación 4"], "c",
         "Esta implicación requiere comprensión profunda del tema."),
        ("¿Cuál es la limitación principal de {topic} en escenarios adversos?",
         ["Limitación A", "Limitación B", "Limitación C", "Limitación D"], "d",
         "Las limitaciones en escenarios adversos son bien conocidas."),
    ],
}


@tool
class QuizGeneratorTool(BaseTool):
    name = "quiz_generator"
    description = (
        "Genera evaluaciones y cuestionarios. "
        "Úsala para crear exámenes, quizzes "
        "y certificados en PDF."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "generate_quiz":
            return self._generate_quiz(**kwargs)
        if action == "grade_responses":
            return self._grade_responses(**kwargs)
        if action == "generate_cert":
            return self._generate_cert(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _generate_quiz(
        self,
        topic: str = "",
        num_questions: int = 5,
        difficulty: str = "medium",
        output_path: str = None,
    ) -> ToolResult:
        if not topic:
            return self._error("El parámetro 'topic' es obligatorio")
        quiz_id = str(uuid4())[:8].upper()
        templates = _QUESTION_TEMPLATES.get(difficulty, _QUESTION_TEMPLATES["medium"])

        import itertools
        template_cycle = itertools.cycle(templates)
        questions = []
        for i in range(num_questions):
            tpl_q, tpl_opts, tpl_ans, tpl_exp = next(template_cycle)
            questions.append({
                "q": tpl_q.format(topic=topic),
                "options": tpl_opts,
                "answer": tpl_ans,
                "explanation": tpl_exp,
            })

        quiz = {
            "id": quiz_id,
            "topic": topic,
            "difficulty": difficulty,
            "num_questions": num_questions,
            "questions": questions,
            "created_at": now_iso(),
        }

        _DATA_DIR.mkdir(parents=True, exist_ok=True)
        quiz_path = _DATA_DIR / f"{quiz_id}.json"
        quiz_path.write_text(
            json.dumps(quiz, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # Attempt PDF generation
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

            if output_path is None:
                output_path = f"data/quizzes/{quiz_id}.pdf"
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            doc = SimpleDocTemplate(output_path, pagesize=letter,
                                    rightMargin=inch, leftMargin=inch,
                                    topMargin=inch, bottomMargin=inch)
            styles = getSampleStyleSheet()
            story = [
                Paragraph(f"QUIZ: {topic.upper()}", styles["Heading1"]),
                Paragraph(f"Dificultad: {difficulty} | Preguntas: {num_questions}",
                          styles["Normal"]),
                Spacer(1, 0.2 * inch),
            ]
            for j, q in enumerate(questions, 1):
                story.append(Paragraph(f"{j}. {q['q']}", styles["Heading3"]))
                for k, opt in zip(["a", "b", "c", "d"], q["options"]):
                    story.append(Paragraph(f"   {k}) {opt}", styles["Normal"]))
                story.append(Spacer(1, 0.1 * inch))
            doc.build(story)
        except ImportError:
            output_path = str(quiz_path)

        return self._success(
            f"Quiz generado: {num_questions} preguntas sobre '{topic}'. "
            f"ID: {quiz_id}",
            raw_data=quiz,
        )

    def _grade_responses(self, quiz_id: str = "", responses: dict = None) -> ToolResult:
        quiz_path = _DATA_DIR / f"{quiz_id}.json"
        if not quiz_path.exists():
            return self._error(f"Quiz '{quiz_id}' no encontrado")
        quiz = json.loads(quiz_path.read_text(encoding="utf-8"))
        questions = quiz.get("questions", [])
        if not questions:
            return self._error("El quiz no tiene preguntas")
        responses = responses or {}
        correctas = 0
        total = len(questions)
        details = []
        for i, q in enumerate(questions):
            key = f"q{i}"
            student_ans = responses.get(key, "")
            correct = q.get("answer", "")
            is_correct = student_ans.lower() == correct.lower()
            if is_correct:
                correctas += 1
            details.append(
                f"P{i+1}: {'✓' if is_correct else '✗'} "
                f"(tuya: {student_ans or 'N/A'}, correcta: {correct})"
            )
        score = (correctas / total) * 100 if total > 0 else 0
        passed = score >= 70
        return self._success(
            f"Score: {score:.0f}% ({correctas}/{total} correctas)\n"
            f"{'Aprobado ✓' if passed else 'Reprobado ✗'}\n\n"
            + "\n".join(details),
            raw_data={"score": score, "passed": passed, "correct": correctas,
                      "total": total},
        )

    def _generate_cert(
        self,
        student_name: str = "",
        course: str = "",
        score: float = 0.0,
        output_path: str = None,
    ) -> ToolResult:
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
        except ImportError:
            return self._error("reportlab no instalado. Ejecuta: pip install reportlab")

        if output_path is None:
            safe = student_name[:20].replace(" ", "_")
            output_path = f"data/certs/cert_{safe}.pdf"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=1.5 * inch, bottomMargin=inch)
        styles = getSampleStyleSheet()
        from tools.utils.dates import now_iso
        fecha = now_iso()[:10]
        story = [
            Paragraph("CERTIFICADO DE COMPLETACIÓN", styles["Heading1"]),
            Spacer(1, 0.3 * inch),
            HRFlowable(width="100%", thickness=2, color=colors.darkblue),
            Spacer(1, 0.3 * inch),
            Paragraph(f"Se certifica que:", styles["Normal"]),
            Spacer(1, 0.1 * inch),
            Paragraph(f"<b>{student_name}</b>", styles["Heading2"]),
            Spacer(1, 0.1 * inch),
            Paragraph(f"Ha completado satisfactoriamente el curso:", styles["Normal"]),
            Paragraph(f"<b>{course}</b>", styles["Heading2"]),
            Spacer(1, 0.2 * inch),
            Paragraph(f"Calificación obtenida: {score:.0f}%", styles["Normal"]),
            Paragraph(f"Fecha: {fecha}", styles["Normal"]),
            Spacer(1, 0.5 * inch),
            HRFlowable(width="50%", thickness=1, color=colors.grey),
            Paragraph("Firma del instructor", styles["Normal"]),
        ]
        try:
            doc.build(story)
        except Exception as e:
            return self._error(f"Error generando certificado: {e}")
        return self._success(
            f"Certificado generado: {output_path}",
            raw_data={"path": output_path, "student": student_name, "score": score},
        )
