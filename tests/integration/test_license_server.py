"""Integration tests for license-server."""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import httpx

# Make license-server importable
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "license-server"))

from db import LicenseDB
from main import app, get_db


# ---------------------------------------------------------------------------
# Fixtures
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


ADMIN_HEADERS = {"X-Admin-Token": "dev-token"}


def _paid_until(days: int) -> str:
    """ISO date string offset from now."""
    dt = datetime.now(timezone.utc) + timedelta(days=days)
    return dt.date().isoformat()


def _iso_ago(hours: int) -> str:
    dt = datetime.now(timezone.utc) - timedelta(hours=hours)
    return dt.isoformat()


async def _create_client(c, db, name="TestCo", pkg="basic", days=30) -> dict:
    res = await c.post(
        "/clients",
        json={"name": name, "package_type": pkg, "paid_until": _paid_until(days)},
        headers=ADMIN_HEADERS,
    )
    assert res.status_code == 200
    return res.json()


async def _heartbeat(c, client_id: str, license_key: str):
    return await c.post("/heartbeat", json={
        "client_id": client_id,
        "license_key": license_key,
        "package_type": "basic",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

async def test_heartbeat_unknown_license_returns_blocked(client):
    c, _ = client
    res = await c.post("/heartbeat", json={
        "client_id": "does-not-exist",
        "license_key": "bad-key",
        "package_type": "basic",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    assert res.status_code == 200
    data = res.json()
    assert data["active"] is False
    assert data["status"] == "blocked"


async def test_heartbeat_new_client_returns_active(client):
    c, db = client
    info = await _create_client(c, db, days=30)
    client_id = info["id"]
    license_key = info["license_key"]

    res = await _heartbeat(c, client_id, license_key)
    assert res.status_code == 200
    data = res.json()
    assert data["active"] is True
    assert data["status"] == "active"


async def test_heartbeat_expired_payment_returns_blocked(client):
    c, db = client
    info = await _create_client(c, db, days=-5)
    client_id = info["id"]
    license_key = info["license_key"]

    db.record_heartbeat(client_id, "127.0.0.1", "basic", "active")
    db._persistent_conn.execute(
        "UPDATE heartbeats SET timestamp=? WHERE client_id=?",
        [_iso_ago(130), client_id],
    )
    db._persistent_conn.commit()

    res = await _heartbeat(c, client_id, license_key)
    assert res.status_code == 200
    data = res.json()
    assert data["active"] is False
    assert data["status"] == "blocked"


async def test_heartbeat_long_offline_but_paid_returns_grace(client):
    c, db = client
    info = await _create_client(c, db, days=30)
    client_id = info["id"]
    license_key = info["license_key"]

    db.record_heartbeat(client_id, "127.0.0.1", "basic", "active")
    db._persistent_conn.execute(
        "UPDATE heartbeats SET timestamp=? WHERE client_id=?",
        [_iso_ago(130), client_id],
    )
    db._persistent_conn.commit()

    res = await _heartbeat(c, client_id, license_key)
    assert res.status_code == 200
    data = res.json()
    assert data["active"] is True
    assert data["status"] == "grace"


async def test_heartbeat_moderate_offline_returns_warning(client):
    c, db = client
    info = await _create_client(c, db, days=30)
    client_id = info["id"]
    license_key = info["license_key"]

    db.record_heartbeat(client_id, "127.0.0.1", "basic", "active")
    db._persistent_conn.execute(
        "UPDATE heartbeats SET timestamp=? WHERE client_id=?",
        [_iso_ago(25), client_id],
    )
    db._persistent_conn.commit()

    res = await _heartbeat(c, client_id, license_key)
    assert res.status_code == 200
    data = res.json()
    assert data["active"] is True
    assert data["status"] == "warning"


async def test_create_client_without_token_returns_403(client):
    c, _ = client
    res = await c.post("/clients", json={
        "name": "No Auth",
        "package_type": "basic",
        "paid_until": _paid_until(30),
    })
    assert res.status_code == 403


async def test_create_client_with_token_returns_license_key(client):
    c, _ = client
    res = await c.post("/clients", json={
        "name": "Auto Key Co",
        "package_type": "pro",
        "paid_until": _paid_until(60),
    }, headers=ADMIN_HEADERS)
    assert res.status_code == 200
    data = res.json()
    assert "license_key" in data
    assert len(data["license_key"]) > 0
    assert "id" in data


async def test_block_client_affects_heartbeat(client):
    c, db = client
    info = await _create_client(c, db, days=30)
    client_id = info["id"]
    license_key = info["license_key"]

    res = await c.post(f"/clients/{client_id}/block", headers=ADMIN_HEADERS)
    assert res.status_code == 200

    res = await _heartbeat(c, client_id, license_key)
    assert res.status_code == 200
    data = res.json()
    assert data["active"] is False
    assert data["status"] == "blocked"


async def test_unblock_restores_access(client):
    c, db = client
    info = await _create_client(c, db, days=30)
    client_id = info["id"]
    license_key = info["license_key"]

    await c.post(f"/clients/{client_id}/block", headers=ADMIN_HEADERS)
    res = await c.post(f"/clients/{client_id}/unblock", headers=ADMIN_HEADERS)
    assert res.status_code == 200

    res = await _heartbeat(c, client_id, license_key)
    assert res.status_code == 200
    data = res.json()
    assert data["active"] is True
    assert data["status"] == "active"


async def test_get_clients_returns_all_with_status(client):
    c, db = client
    await _create_client(c, db, name="Alpha", days=30)
    await _create_client(c, db, name="Beta", days=30)

    res = await c.get("/clients", headers=ADMIN_HEADERS)
    assert res.status_code == 200
    clients = res.json()
    assert len(clients) == 2
    for cl in clients:
        assert "status" in cl
        assert cl["status"] in {"active", "warning", "grace", "blocked"}
