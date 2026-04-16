import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nomi-mx.com", "https://www.nomi-mx.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def _send_email(to: str, subject: str, html: str) -> None:
    """Envía email usando la API HTTP de Resend."""
    import requests

    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("FROM_EMAIL", "hola@nomi-mx.com")

    if not api_key:
        raise ValueError("RESEND_API_KEY not configured")

    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "from": from_email,
            "to": [to],
            "subject": subject,
            "html": html
        }
    )

    if response.status_code != 200:
        raise ValueError(f"Resend API error: {response.text}")


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
            html=_email_template(client_name, license_key, download_url),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar email: {str(e)}")

    return {
        "ok": True,
        "message": f"Email enviado a {email_to}",
        "download_url": download_url,
    }


# ---------------------------------------------------------------------------
# Leads endpoints
# ---------------------------------------------------------------------------

def _init_leads_table(db_path: str) -> None:
    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre    TEXT NOT NULL,
            email     TEXT NOT NULL,
            mensaje   TEXT,
            plan      TEXT,
            agentes   TEXT,
            precio    REAL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.on_event("startup")
async def _startup() -> None:
    db = get_db()
    _init_leads_table(db.db_path)


@app.post("/leads", status_code=201)
async def create_lead(request: Request, db: LicenseDB = Depends(get_db)):
    import json
    import sqlite3
    body = await request.json()
    nombre = body.get("nombre", "").strip()
    email = body.get("email", "").strip()
    if not nombre or not email:
        raise HTTPException(status_code=422, detail="nombre y email son requeridos")

    agentes = body.get("agentes", [])
    if isinstance(agentes, list):
        agentes_str = json.dumps(agentes)
    else:
        agentes_str = str(agentes)

    now = datetime.now(timezone.utc).isoformat()
    conn = sqlite3.connect(db.db_path)
    cur = conn.execute(
        "INSERT INTO leads (nombre, email, mensaje, plan, agentes, precio, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            nombre,
            email,
            body.get("mensaje", ""),
            body.get("plan", ""),
            agentes_str,
            body.get("precio_estimado"),
            now,
        ),
    )
    lead_id = cur.lastrowid
    conn.commit()
    conn.close()
    return {"id": lead_id, "ok": True}


@app.get("/leads", dependencies=[Depends(verify_admin)])
async def list_leads(db: LicenseDB = Depends(get_db)):
    import json
    import sqlite3
    conn = sqlite3.connect(db.db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM leads ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    result = []
    for row in rows:
        d = dict(row)
        try:
            d["agentes"] = json.loads(d["agentes"])
        except (json.JSONDecodeError, TypeError):
            d["agentes"] = []
        result.append(d)
    return result


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
