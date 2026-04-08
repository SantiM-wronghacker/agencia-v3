"""Extended integration tests for license-server."""
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "license-server"))

from db import LicenseDB
from main import app, get_db

ADMIN_HEADERS = {"X-Admin-Token": "dev-token"}
ADMIN_TOKEN = "dev-token"


# ---------------------------------------------------------------------------
# Fixtures (local — same pattern as test_license_server.py)
# ---------------------------------------------------------------------------

@pytest.fixture
def mem_db() -> LicenseDB:
    return LicenseDB(db_path=":memory:")


@pytest.fixture
async def client(mem_db: LicenseDB):
    app.dependency_overrides[get_db] = lambda: mem_db
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c, mem_db
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _paid_until(days: int) -> str:
    dt = datetime.now(timezone.utc) + timedelta(days=days)
    return dt.date().isoformat()


async def _create_client(c, name="TestCo", pkg="basic", days=30) -> dict:
    res = await c.post(
        "/clients",
        json={"name": name, "package_type": pkg, "paid_until": _paid_until(days)},
        headers=ADMIN_HEADERS,
    )
    assert res.status_code == 200
    return res.json()


async def _heartbeat(c, client_id: str, license_key: str):
    return await c.post(
        "/heartbeat",
        json={
            "client_id": client_id,
            "license_key": license_key,
            "package_type": "basic",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

async def test_get_client_detail_includes_heartbeat_list(client):
    c, db = client
    data = await _create_client(c)
    cid, key = data["id"], data["license_key"]

    await _heartbeat(c, cid, key)
    await _heartbeat(c, cid, key)

    res = await c.get(f"/clients/{cid}", headers=ADMIN_HEADERS)
    assert res.status_code == 200
    body = res.json()
    assert "heartbeats" in body
    assert len(body["heartbeats"]) >= 2


async def test_patch_client_updates_paid_until(client):
    c, db = client
    data = await _create_client(c)
    cid = data["id"]

    res = await c.patch(
        f"/clients/{cid}",
        json={"paid_until": "2027-01-01"},
        headers=ADMIN_HEADERS,
    )
    assert res.status_code == 200

    detail = await c.get(f"/clients/{cid}", headers=ADMIN_HEADERS)
    assert detail.status_code == 200
    assert detail.json()["paid_until"] == "2027-01-01"


async def test_patch_client_updates_package_type(client):
    c, db = client
    data = await _create_client(c, pkg="basic")
    cid = data["id"]

    res = await c.patch(
        f"/clients/{cid}",
        json={"package_type": "pro"},
        headers=ADMIN_HEADERS,
    )
    assert res.status_code == 200

    detail = await c.get(f"/clients/{cid}", headers=ADMIN_HEADERS)
    assert detail.json()["package_type"] == "pro"


async def test_dashboard_without_token_returns_403(client):
    c, db = client
    res = await c.get("/dashboard")
    assert res.status_code == 403


async def test_dashboard_with_wrong_token_returns_403(client):
    c, db = client
    res = await c.get("/dashboard?token=token-incorrecto")
    assert res.status_code == 403


async def test_dashboard_with_correct_token_returns_html(client):
    c, db = client
    res = await c.get(f"/dashboard?token={ADMIN_TOKEN}")
    assert res.status_code == 200
    assert "text/html" in res.headers.get("content-type", "")
    body = res.text.lower()
    assert "<html" in body or "<table" in body or "license" in body


async def test_block_already_blocked_is_idempotent(client):
    c, db = client
    data = await _create_client(c)
    cid, key = data["id"], data["license_key"]

    # First block
    r1 = await c.post(f"/clients/{cid}/block", headers=ADMIN_HEADERS)
    assert r1.status_code == 200

    # Second block — must not error
    r2 = await c.post(f"/clients/{cid}/block", headers=ADMIN_HEADERS)
    assert r2.status_code == 200

    # Heartbeat still reports blocked
    hb = await _heartbeat(c, cid, key)
    assert hb.json()["active"] is False


async def test_unblock_active_client_is_idempotent(client):
    c, db = client
    data = await _create_client(c)
    cid = data["id"]

    # Client is already active — unblock should succeed silently
    res = await c.post(f"/clients/{cid}/unblock", headers=ADMIN_HEADERS)
    assert res.status_code == 200
    assert res.json()["ok"] is True


async def test_list_clients_shows_computed_status(client):
    c, db = client
    # Active client
    await _create_client(c, name="Active Corp", days=30)
    # Expired client
    await _create_client(c, name="Expired Corp", days=-10)

    res = await c.get("/clients", headers=ADMIN_HEADERS)
    assert res.status_code == 200
    clients = res.json()
    assert len(clients) >= 2
    statuses = {cl["name"]: cl["status"] for cl in clients}
    assert "Active Corp" in statuses
    assert "Expired Corp" in statuses


async def test_heartbeat_records_in_db(client):
    c, db = client
    data = await _create_client(c)
    cid, key = data["id"], data["license_key"]

    hb_res = await _heartbeat(c, cid, key)
    assert hb_res.status_code == 200

    detail = await c.get(f"/clients/{cid}", headers=ADMIN_HEADERS)
    assert detail.status_code == 200
    heartbeats = detail.json()["heartbeats"]
    assert len(heartbeats) >= 1
    assert heartbeats[0]["client_id"] == cid
