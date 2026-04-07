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

    return HeartbeatResponse(
        active=active,
        status=status,
        message=message,
        days_remaining=days_remaining,
        hours_offline=hours_offline,
    )


# ---------------------------------------------------------------------------
# Admin endpoints
# ---------------------------------------------------------------------------

@app.post("/clients", dependencies=[Depends(verify_admin)])
async def create_client(body: ClientCreate, db: LicenseDB = Depends(get_db)):
    license_key = body.license_key or str(uuid.uuid4()).replace("-", "")
    client_id = db.create_client(
        name=body.name,
        license_key=license_key,
        package_type=body.package_type,
        paid_until=body.paid_until,
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
    if db.get_client(client_id) is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.update_client(
        client_id,
        active=int(body.active) if body.active is not None else None,
        paid_until=body.paid_until,
        package_type=body.package_type,
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
    db.update_client(client_id, active=1)
    return {"ok": True}


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(token: str = Query(default="")):
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
