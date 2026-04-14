import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse

load_dotenv()

# Allow running from project root: python -m license-server.main
sys.path.insert(0, str(Path(__file__).parent))

from auth import verify_admin
from db import LicenseDB
from models import (
    ClientCreate,
    ClientUpdate,
    HeartbeatRequest,
    HeartbeatResponse,
    SendLinkRequest,
    ValidateResponse,
)

app = FastAPI(title="License Server", version="1.0.0")

# ---------------------------------------------------------------------------
# DB dependency
# ---------------------------------------------------------------------------

_db: LicenseDB | None = None


def get_db() -> LicenseDB:
    global _db
    if _db is None:
        _db = LicenseDB()
    return _db


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _send_email(to: str, subject: str, body: str, html: bool = False) -> None:
    """Envía email usando SMTP."""
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not all([smtp_host, smtp_user, smtp_password]):
        raise ValueError("SMTP credentials not configured")

    msg = MIMEMultipart("alternative")
    msg["From"] = smtp_user
    msg["To"] = to
    msg["Subject"] = subject

    mime_type = "html" if html else "plain"
    msg.attach(MIMEText(body, mime_type, "utf-8"))

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(smtp_user, smtp_password)
        smtp.sendmail(smtp_user, to, msg.as_string())


def _email_template(client_name: str, license_key: str, download_url: str) -> str:
    """Template HTML para email de descarga."""
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2>¡Bienvenido {client_name}!</h2>
        <p>Tu Agencia IA está lista para usar. Descárgala e ingresa tu clave de licencia:</p>

        <div style="background-color: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <p><strong>Clave de Licencia:</strong></p>
            <code style="font-size: 14px; word-break: break-all;">{license_key}</code>
        </div>

        <p>
            <a href="{download_url}"
               style="background-color: #007bff; color: white; padding: 12px 24px;
                      text-decoration: none; border-radius: 4px; display: inline-block;">
                Descargar Agencia IA
            </a>
        </p>

        <p>Guarda tu clave de licencia en un lugar seguro. La necesitarás para activar la aplicación.</p>
        <p>¿Preguntas? Contacta a: <a href="mailto:support@agencia-ia.com">support@agencia-ia.com</a></p>

        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
        <p style="font-size: 12px; color: #666;">© 2026 Agencia IA. Todos los derechos reservados.</p>
    </body>
    </html>
    """


def _compute_status(client: dict, last_hb: dict | None) -> tuple[bool, str, str, int, int]:
    """Returns (active, status, message, days_remaining, hours_offline)."""
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    paid_until = datetime.fromisoformat(client["paid_until"].replace("Z", ""))

    hours_offline = 0
    if last_hb:
        last_ts = datetime.fromisoformat(last_hb["timestamp"].replace("Z", ""))
        if last_ts.tzinfo is not None:
            last_ts = last_ts.replace(tzinfo=None)
        hours_offline = (now - last_ts).total_seconds() / 3600

    if paid_until.tzinfo is not None:
        paid_until = paid_until.replace(tzinfo=None)

    payment_expired = now > paid_until
    days_remaining = max(0, (paid_until - now).days)

    if not client["active"]:
        return False, "blocked", "Servicio suspendido. Contacta soporte.", days_remaining, int(hours_offline)

    if hours_offline > 120 and payment_expired:
        return False, "blocked", "Servicio suspendido. Contacta soporte.", days_remaining, int(hours_offline)

    if hours_offline > 120:
        days_grace = max(0, 30 - int((now - datetime.fromisoformat(last_hb["timestamp"].replace("Z", "")).replace(tzinfo=None)).days))
        return True, "grace", f"Modo offline. Reconecta antes de {days_grace} días.", days_remaining, int(hours_offline)

    if hours_offline > 24:
        return True, "warning", f"Sin conexión hace {int(hours_offline)}h. Verifica tu internet.", days_remaining, int(hours_offline)

    return True, "active", "", days_remaining, int(hours_offline)


# ---------------------------------------------------------------------------
# Public endpoint
# ---------------------------------------------------------------------------

@app.post("/heartbeat", response_model=HeartbeatResponse)
async def heartbeat(req: HeartbeatRequest, request: Request, db: LicenseDB = Depends(get_db)):
    client = db.get_client_by_key(req.license_key)

    if client is None or client["id"] != req.client_id:
        return HeartbeatResponse(
            active=False,
            status="blocked",
            message="Licencia no válida.",
            days_remaining=0,
            hours_offline=0,
        )

    last_hb = db.get_last_heartbeat(client["id"])
    active, status, message, days_remaining, hours_offline = _compute_status(client, last_hb)

    ip = request.client.host if request.client else "unknown"
    db.record_heartbeat(client["id"], ip, req.package_type, status)
    db.update_last_heartbeat(client["id"], req.timestamp)

    return HeartbeatResponse(
        active=active,
        status=status,
        message=message,
        days_remaining=days_remaining,
        hours_offline=hours_offline,
    )


# ---------------------------------------------------------------------------
# Public validation endpoint
# ---------------------------------------------------------------------------

@app.get("/validate/{license_key}", response_model=ValidateResponse)
async def validate_license(license_key: str, db: LicenseDB = Depends(get_db)):
    """Valida una licencia desde la app Electron."""
    import json

    client = db.get_client_by_key(license_key)
    if client is None:
        return ValidateResponse(
            valid=False,
            status="invalid",
            message="Licencia no encontrada",
        )

    last_hb = db.get_last_heartbeat(client["id"])
    active, status, message, _, _ = _compute_status(client, last_hb)

    if not active or status == "blocked":
        return ValidateResponse(
            valid=False,
            status=status,
            client_name=client["name"],
            message=message or "Acceso denegado",
        )

    agentes = []
    try:
        agentes = json.loads(client.get("agentes", "[]"))
    except (json.JSONDecodeError, TypeError):
        agentes = []

    return ValidateResponse(
        valid=True,
        status=status,
        client_name=client["name"],
        plan=client.get("package_type", "basic"),
        agentes=agentes,
        message=message,
    )


# ---------------------------------------------------------------------------
# Admin endpoints
# ---------------------------------------------------------------------------

@app.post("/clients", dependencies=[Depends(verify_admin)])
async def create_client(body: ClientCreate, db: LicenseDB = Depends(get_db)):
    import json
    license_key = body.license_key or str(uuid.uuid4()).replace("-", "")
    agentes_json = json.dumps(body.agentes or [])
    client_id = db.create_client(
        name=body.name,
        email=body.email,
        license_key=license_key,
        package_type=body.package_type,
        paid_until=body.paid_until,
        agentes=agentes_json,
    )
    return {"id": client_id, "license_key": license_key}


@app.get("/clients", dependencies=[Depends(verify_admin)])
async def list_clients(db: LicenseDB = Depends(get_db)):
    clients = db.get_all_clients()
    result = []
    for c in clients:
        last_hb = db.get_last_heartbeat(c["id"])
        _, status, _, days_remaining, hours_offline = _compute_status(c, last_hb)
        result.append({
            **c,
            "status": status,
            "days_remaining": days_remaining,
            "hours_offline": hours_offline,
            "last_heartbeat": last_hb["timestamp"] if last_hb else None,
        })
    return result


@app.get("/clients/{client_id}", dependencies=[Depends(verify_admin)])
async def get_client(client_id: str, db: LicenseDB = Depends(get_db)):
    client = db.get_client(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    last_hb = db.get_last_heartbeat(client_id)
    _, status, _, days_remaining, hours_offline = _compute_status(client, last_hb)
    heartbeats = db.get_client_heartbeats(client_id, limit=10)
    return {
        **client,
        "status": status,
        "days_remaining": days_remaining,
        "hours_offline": hours_offline,
        "heartbeats": heartbeats,
    }


@app.patch("/clients/{client_id}", dependencies=[Depends(verify_admin)])
async def update_client(client_id: str, body: ClientUpdate, db: LicenseDB = Depends(get_db)):
    import json

    if db.get_client(client_id) is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Prepare agentes field
    agentes = None
    if body.agentes is not None:
        if isinstance(body.agentes, list):
            agentes = json.dumps(body.agentes)
        else:
            agentes = body.agentes

    db.update_client(
        client_id,
        active=int(body.active) if body.active is not None else None,
        paid_until=body.paid_until,
        package_type=body.package_type,
        status=body.status,
        agentes=agentes,
        notes=body.notes,
    )
    return {"ok": True}


@app.post("/clients/{client_id}/block", dependencies=[Depends(verify_admin)])
async def block_client(client_id: str, db: LicenseDB = Depends(get_db)):
    if db.get_client(client_id) is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.update_client(client_id, active=0)
    return {"ok": True}


@app.post("/clients/{client_id}/unblock", dependencies=[Depends(verify_admin)])
async def unblock_client(client_id: str, db: LicenseDB = Depends(get_db)):
    if db.get_client(client_id) is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.update_client(client_id, active=1, status="active")
    return {"ok": True}


@app.post("/clients/{client_id}/send-link", dependencies=[Depends(verify_admin)])
async def send_download_link(
    client_id: str,
    body: SendLinkRequest,
    db: LicenseDB = Depends(get_db),
):
    """Envía email con link de descarga + license_key al cliente."""
    client = db.get_client(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Template del link de descarga
    download_url = body.download_url or os.getenv(
        "DOWNLOAD_LINK_TEMPLATE",
        "https://tu-dominio.com/download?key={license_key}",
    ).format(license_key=client["license_key"])

    # Datos del email
    email_to = client["email"]
    client_name = client["name"]
    license_key = client["license_key"]

    # Enviar email
    try:
        _send_email(
            to=email_to,
            subject=f"Tu Agencia IA — Descarga y Licencia",
            body=_email_template(client_name, license_key, download_url),
            html=True,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar email: {str(e)}")

    return {
        "ok": True,
        "message": f"Email enviado a {email_to}",
        "download_url": download_url,
    }


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(token: str = Query(default="")):
    if not token or token != os.getenv("ADMIN_TOKEN", "dev-token"):
        raise HTTPException(status_code=403, detail="Token inválido")
    html_path = Path(__file__).parent / "dashboard.html"
    html = html_path.read_text(encoding="utf-8")
    # Inject token into the page so JS can use it
    html = html.replace("__INJECTED_TOKEN__", token)
    return HTMLResponse(content=html)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
