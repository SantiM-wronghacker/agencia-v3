import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from tools.base import BaseTool, ToolResult, tool


@tool
class SMTPTool(BaseTool):
    name = "smtp_email"
    description = (
        "Envía emails via SMTP. "
        "Úsala para enviar correos a clientes o equipos."
    )

    def run(self, action: str = "", **kwargs) -> ToolResult:
        if action == "send":
            return self._send(**kwargs)
        if action == "send_bulk":
            return self._send_bulk(**kwargs)
        return self._error(f"Acción '{action}' no soportada")

    def _check_credentials(self) -> ToolResult | None:
        for key in ("smtp_host", "smtp_port", "smtp_user", "smtp_password"):
            if not self.credentials.get(key):
                return self._error(f"Credencial {key} no configurada")
        return None

    def _build_message(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = False,
    ) -> MIMEMultipart:
        msg = MIMEMultipart("alternative")
        msg["From"] = self.credentials["smtp_user"]
        msg["To"] = to
        msg["Subject"] = subject
        mime_type = "html" if html else "plain"
        msg.attach(MIMEText(body, mime_type, "utf-8"))
        return msg

    def _connect(self) -> smtplib.SMTP:
        host = self.credentials["smtp_host"]
        port = int(self.credentials["smtp_port"])
        user = self.credentials["smtp_user"]
        password = self.credentials["smtp_password"]

        smtp = smtplib.SMTP(host, port, timeout=30)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(user, password)
        return smtp

    def _send(
        self,
        to: str = "",
        subject: str = "",
        body: str = "",
        html: bool = False,
    ) -> ToolResult:
        err = self._check_credentials()
        if err:
            return err
        if not to:
            return self._error("Parámetro to (destinatario) requerido")
        if not subject:
            return self._error("Parámetro subject (asunto) requerido")

        try:
            msg = self._build_message(to, subject, body, html)
            smtp = self._connect()
            smtp.sendmail(self.credentials["smtp_user"], to, msg.as_string())
            smtp.quit()
        except Exception as e:
            return self._error(f"Error al enviar email: {e}")

        return self._success(
            f"Email enviado a {to}. Asunto: {subject}",
            raw_data={"to": to, "subject": subject},
        )

    def _send_bulk(
        self,
        recipients: list = None,
        subject: str = "",
        body: str = "",
        html: bool = False,
    ) -> ToolResult:
        err = self._check_credentials()
        if err:
            return err
        if not recipients:
            return self._error("Parámetro recipients (lista de destinatarios) requerido")
        if not subject:
            return self._error("Parámetro subject (asunto) requerido")

        sent = []
        failed = []
        try:
            smtp = self._connect()
            for to in recipients:
                try:
                    msg = self._build_message(to, subject, body, html)
                    smtp.sendmail(self.credentials["smtp_user"], to, msg.as_string())
                    sent.append(to)
                except Exception as e:
                    failed.append(f"{to} ({e})")
            smtp.quit()
        except Exception as e:
            return self._error(f"Error de conexión SMTP: {e}")

        lines = [f"Envío masivo completado. Enviados: {len(sent)}/{len(recipients)}"]
        if failed:
            lines.append(f"Fallidos: {', '.join(failed)}")
        return self._success(
            "\n".join(lines),
            raw_data={"sent": sent, "failed": failed},
        )
