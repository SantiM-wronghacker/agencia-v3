"""Tests para license-server endpoints."""
import json
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from db import LicenseDB


@pytest.fixture
def db_in_memory():
    """DB en memoria compartida para tests."""
    return LicenseDB(db_path=":memory:")


@pytest.fixture
def client(db_in_memory):
    """Cliente de test que usa la DB en memoria."""
    from main import app, get_db

    # Inyecta la DB en memoria en get_db
    app.dependency_overrides[get_db] = lambda: db_in_memory
    return TestClient(app)


@pytest.fixture
def admin_headers():
    """Headers con token de admin."""
    return {"X-Admin-Token": "dev-token"}


@pytest.fixture
def test_client_data(db_in_memory):
    """Crea un cliente de test en la DB."""
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=30)).date().isoformat()
    client_id = db_in_memory.create_client(
        name="Test Company",
        email="test@example.com",
        license_key="test-key-123",
        package_type="core",
        paid_until=tomorrow,
        agentes='["content_pipeline", "sales_pipeline"]',
    )
    return client_id, db_in_memory.get_client(client_id)


# ---------------------------------------------------------------------------
# Tests — Crear Cliente
# ---------------------------------------------------------------------------


def test_create_client(client, admin_headers):
    """POST /clients — crear cliente."""
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=30)).date().isoformat()
    response = client.post(
        "/clients",
        json={
            "name": "Acme Corp",
            "email": "admin@acme.com",
            "package_type": "prime",
            "paid_until": tomorrow,
            "agentes": ["content_pipeline", "sales_pipeline"],
        },
        headers=admin_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "license_key" in data
    assert len(data["license_key"]) > 0


def test_create_client_without_auth(client):
    """POST /clients sin auth debe fallar."""
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=30)).date().isoformat()
    response = client.post(
        "/clients",
        json={
            "name": "Acme Corp",
            "email": "admin@acme.com",
            "package_type": "prime",
            "paid_until": tomorrow,
        },
    )
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# Tests — Listar Clientes
# ---------------------------------------------------------------------------


def test_list_clients(client, admin_headers, test_client_data):
    """GET /clients — listar clientes."""
    response = client.get("/clients", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_list_clients_includes_status(client, admin_headers, test_client_data):
    """GET /clients incluye status computado."""
    response = client.get("/clients", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    client_data = data[0]
    assert "status" in client_data
    assert client_data["status"] in ["active", "warning", "grace", "blocked"]


# ---------------------------------------------------------------------------
# Tests — Detalle de Cliente
# ---------------------------------------------------------------------------


def test_get_client(client, admin_headers, test_client_data):
    """GET /clients/{id} — detalle de cliente."""
    client_id, _ = test_client_data
    response = client.get(f"/clients/{client_id}", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == client_id
    assert data["name"] == "Test Company"
    assert data["email"] == "test@example.com"


def test_get_client_not_found(client, admin_headers):
    """GET /clients/{id} — cliente no existe."""
    response = client.get("/clients/nonexistent", headers=admin_headers)
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Tests — Editar Cliente
# ---------------------------------------------------------------------------


def test_update_client(client, admin_headers, test_client_data):
    """PATCH /clients/{id} — editar cliente."""
    client_id, _ = test_client_data
    new_date = (datetime.now(timezone.utc) + timedelta(days=60)).date().isoformat()
    response = client.patch(
        f"/clients/{client_id}",
        json={
            "package_type": "lite",
            "paid_until": new_date,
            "notes": "Cliente premium",
        },
        headers=admin_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True


def test_update_client_agentes(client, admin_headers, test_client_data):
    """PATCH /clients/{id} — actualizar agentes."""
    client_id, _ = test_client_data
    response = client.patch(
        f"/clients/{client_id}",
        json={"agentes": ["blog_publisher", "email_campaign"]},
        headers=admin_headers,
    )
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# Tests — Bloquear/Desbloquear
# ---------------------------------------------------------------------------


def test_block_client(client, admin_headers, test_client_data):
    """POST /clients/{id}/block — bloquear cliente."""
    client_id, _ = test_client_data
    response = client.post(f"/clients/{client_id}/block", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_unblock_client(client, admin_headers, test_client_data):
    """POST /clients/{id}/unblock — desbloquear cliente."""
    client_id, _ = test_client_data
    # Primero bloquea
    client.post(f"/clients/{client_id}/block", headers=admin_headers)
    # Luego desbloquea
    response = client.post(f"/clients/{client_id}/unblock", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["ok"] is True


# ---------------------------------------------------------------------------
# Tests — Validar Licencia (público)
# ---------------------------------------------------------------------------


def test_validate_license_valid(client, test_client_data):
    """GET /validate/{license_key} — licencia válida."""
    _, client_data = test_client_data
    license_key = client_data["license_key"]
    response = client.get(f"/validate/{license_key}")
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["status"] in ["active", "warning"]
    assert data["client_name"] == "Test Company"
    assert data["plan"] == "core"
    assert isinstance(data["agentes"], list)


def test_validate_license_invalid(client):
    """GET /validate/{license_key} — licencia inválida."""
    response = client.get("/validate/invalid-key-xyz")
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert data["status"] == "invalid"


def test_validate_license_blocked(client, admin_headers, test_client_data):
    """GET /validate/{license_key} — cliente bloqueado."""
    client_id, client_data = test_client_data
    license_key = client_data["license_key"]

    # Bloquea el cliente
    client.post(f"/clients/{client_id}/block", headers=admin_headers)

    # Intenta validar
    response = client.get(f"/validate/{license_key}")
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert data["status"] == "blocked"


# ---------------------------------------------------------------------------
# Tests — Heartbeat (público)
# ---------------------------------------------------------------------------


def test_heartbeat_valid(client, test_client_data):
    """POST /heartbeat — heartbeat válido."""
    client_id, client_data = test_client_data
    now_iso = datetime.now(timezone.utc).isoformat()
    response = client.post(
        "/heartbeat",
        json={
            "client_id": client_id,
            "license_key": client_data["license_key"],
            "package_type": "core",
            "timestamp": now_iso,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["active"] is True
    assert data["status"] in ["active", "warning"]
    assert data["days_remaining"] > 0


def test_heartbeat_invalid_key(client):
    """POST /heartbeat — licencia inválida."""
    now_iso = datetime.now(timezone.utc).isoformat()
    response = client.post(
        "/heartbeat",
        json={
            "client_id": "some-id",
            "license_key": "invalid",
            "package_type": "basic",
            "timestamp": now_iso,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["active"] is False


# ---------------------------------------------------------------------------
# Tests — Integración: crear, validar, bloquear
# ---------------------------------------------------------------------------


def test_full_client_lifecycle(client, admin_headers):
    """Flujo completo: crear → validar → bloquear → validar."""
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=30)).date().isoformat()

    # 1. Crear cliente
    create_resp = client.post(
        "/clients",
        json={
            "name": "Lifecycle Test",
            "email": "lifecycle@test.com",
            "package_type": "basic",
            "paid_until": tomorrow,
            "agentes": ["sales_pipeline"],
        },
        headers=admin_headers,
    )
    assert create_resp.status_code == 200
    client_id = create_resp.json()["id"]
    license_key = create_resp.json()["license_key"]

    # 2. Validar licencia (debe ser válida)
    validate_resp = client.get(f"/validate/{license_key}")
    assert validate_resp.status_code == 200
    assert validate_resp.json()["valid"] is True

    # 3. Bloquear cliente
    block_resp = client.post(f"/clients/{client_id}/block", headers=admin_headers)
    assert block_resp.status_code == 200

    # 4. Validar licencia (debe ser inválida ahora)
    validate_resp = client.get(f"/validate/{license_key}")
    assert validate_resp.status_code == 200
    assert validate_resp.json()["valid"] is False
    assert validate_resp.json()["status"] == "blocked"

    # 5. Desbloquear cliente
    unblock_resp = client.post(f"/clients/{client_id}/unblock", headers=admin_headers)
    assert unblock_resp.status_code == 200

    # 6. Validar licencia (debe ser válida de nuevo)
    validate_resp = client.get(f"/validate/{license_key}")
    assert validate_resp.status_code == 200
    assert validate_resp.json()["valid"] is True
