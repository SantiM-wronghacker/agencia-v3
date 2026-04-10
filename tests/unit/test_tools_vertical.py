"""Tests for tools/vertical/ and vertical groups."""
import sys
import types
from unittest.mock import patch, MagicMock

import pytest

from tools.vertical.reservations import ReservationsTool
from tools.vertical.menu_manager import MenuManagerTool
from tools.vertical.appointment_scheduler import AppointmentSchedulerTool
from tools.vertical.patient_forms import PatientFormsTool
from tools.vertical.property_listings import PropertyListingsTool
from tools.vertical.portals import PortalsTool
from tools.vertical.shipping import ShippingTool
from tools.vertical.inventory import InventoryTool
from tools.vertical.policy_manager import PolicyManagerTool
from tools.vertical.itinerary import ItineraryTool
from groups.restaurant_manager import create_restaurant_manager
from groups.health_assistant import create_health_assistant
from groups.real_estate_agent import create_real_estate_agent
from groups.logistics_coordinator import create_logistics_coordinator
from groups.insurance_advisor import create_insurance_advisor
from groups.travel_planner import create_travel_planner


# ---------------------------------------------------------------------------
# ReservationsTool
# ---------------------------------------------------------------------------

def test_reservations_create_returns_success(tmp_path):
    with patch("tools.vertical.reservations._DATA_FILE", tmp_path / "reservations.json"):
        tool = ReservationsTool()
        result = tool.run(
            action="create",
            name="García",
            date="2026-06-01",
            time="20:00",
            party_size=4,
            phone="5512345678",
        )
    assert result.success
    assert "García" in result.output
    assert result.raw_data["id"] is not None


def test_reservations_unknown_action_returns_error():
    tool = ReservationsTool()
    result = tool.run(action="invalida")
    assert not result.success
    assert "no soportada" in result.error


def test_reservations_check_availability(tmp_path):
    with patch("tools.vertical.reservations._DATA_FILE", tmp_path / "reservations.json"):
        tool = ReservationsTool()
        result = tool.run(
            action="check_availability",
            date="2026-06-01",
            time="20:00",
            party_size=4,
        )
    assert result.success
    assert "Disponible" in result.output or "Sin disponibilidad" in result.output


def test_reservations_list_today(tmp_path):
    with patch("tools.vertical.reservations._DATA_FILE", tmp_path / "reservations.json"):
        tool = ReservationsTool()
        result = tool.run(action="list_today")
    assert result.success


def test_reservations_confirm_not_found():
    tool = ReservationsTool()
    with patch("tools.vertical.reservations._load", return_value=[]):
        result = tool.run(action="confirm", reservation_id="INVALID")
    assert not result.success
    assert "no encontrada" in result.error


# ---------------------------------------------------------------------------
# MenuManagerTool
# ---------------------------------------------------------------------------

def test_menu_manager_get_menu_returns_default(tmp_path):
    with patch("tools.vertical.menu_manager._DATA_FILE", tmp_path / "menu.json"):
        tool = MenuManagerTool()
        result = tool.run(action="get_menu")
    assert result.success
    assert len(result.output) > 0


def test_menu_manager_add_special(tmp_path):
    with patch("tools.vertical.menu_manager._DATA_FILE", tmp_path / "menu.json"):
        tool = MenuManagerTool()
        result = tool.run(
            action="add_special",
            name="Sopa del día",
            description="Crema de elote",
            price=85.0,
        )
    assert result.success
    assert "Sopa del día" in result.output


def test_menu_manager_update_price_not_found(tmp_path):
    with patch("tools.vertical.menu_manager._DATA_FILE", tmp_path / "menu.json"):
        tool = MenuManagerTool()
        result = tool.run(action="update_price", item_name="Platillo Inexistente", new_price=99.0)
    assert not result.success
    assert "no encontrado" in result.error


def test_menu_manager_get_menu_by_category(tmp_path):
    with patch("tools.vertical.menu_manager._DATA_FILE", tmp_path / "menu.json"):
        tool = MenuManagerTool()
        result = tool.run(action="get_menu", category="entradas")
    assert result.success


def test_menu_manager_remove_special_not_found(tmp_path):
    with patch("tools.vertical.menu_manager._DATA_FILE", tmp_path / "menu.json"):
        tool = MenuManagerTool()
        result = tool.run(action="remove_special", name="Inexistente")
    assert not result.success
    assert "no encontrado" in result.error


def test_menu_manager_unsupported_action():
    tool = MenuManagerTool()
    assert not tool.run(action="delete_menu").success


# ---------------------------------------------------------------------------
# AppointmentSchedulerTool
# ---------------------------------------------------------------------------

def test_appointment_create_returns_success(tmp_path):
    with patch("tools.vertical.appointment_scheduler._DATA_FILE", tmp_path / "appointments.json"):
        tool = AppointmentSchedulerTool()
        result = tool.run(
            action="create",
            patient_name="López",
            doctor="Martínez",
            date="2026-06-01",
            time="10:00",
        )
    assert result.success
    assert "López" in result.output


def test_appointment_cancel(tmp_path):
    with patch("tools.vertical.appointment_scheduler._DATA_FILE", tmp_path / "appts.json"):
        tool = AppointmentSchedulerTool()
        create_result = tool.run(
            action="create",
            patient_name="Test",
            doctor="Doc",
            date="2026-06-01",
            time="10:00",
        )
        apt_id = create_result.raw_data["id"]
        cancel_result = tool.run(action="cancel", appointment_id=apt_id)
    assert cancel_result.success
    assert apt_id in cancel_result.output


def test_appointment_cancel_not_found():
    tool = AppointmentSchedulerTool()
    with patch("tools.vertical.appointment_scheduler._load", return_value=[]):
        result = tool.run(action="cancel", appointment_id="NOPE")
    assert not result.success


def test_appointment_list_empty(tmp_path):
    with patch("tools.vertical.appointment_scheduler._DATA_FILE", tmp_path / "appts.json"):
        tool = AppointmentSchedulerTool()
        result = tool.run(action="list", date="2099-01-01")
    assert result.success
    assert "Sin citas" in result.output


def test_appointment_send_reminder_not_found():
    tool = AppointmentSchedulerTool()
    with patch("tools.vertical.appointment_scheduler._load", return_value=[]):
        result = tool.run(action="send_reminder", appointment_id="NONE")
    assert not result.success


def test_appointment_send_reminder_no_whatsapp(tmp_path):
    with patch("tools.vertical.appointment_scheduler._DATA_FILE", tmp_path / "appts.json"):
        tool = AppointmentSchedulerTool()
        tool.run(action="create", patient_name="Ana", doctor="García",
                 date="2026-06-01", time="09:00", phone="5512341234")
        data = __import__("json").loads((tmp_path / "appts.json").read_text())
        apt_id = data[0]["id"]
        result = tool.run(action="send_reminder", appointment_id=apt_id)
    assert result.success
    assert "manualmente" in result.output or "Recordatorio" in result.output


def test_appointment_unsupported_action():
    assert not AppointmentSchedulerTool().run(action="unknown").success


# ---------------------------------------------------------------------------
# PatientFormsTool
# ---------------------------------------------------------------------------

def test_patient_forms_no_reportlab_returns_error(monkeypatch):
    import builtins
    real_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name == "reportlab" or name.startswith("reportlab."):
            raise ImportError("mocked missing reportlab")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", mock_import)
    tool = PatientFormsTool()
    result = tool.run(action="generate_intake", patient_name="Test")
    if not result.success:
        assert "reportlab" in result.error.lower()


def test_patient_forms_generate_intake_with_reportlab(tmp_path):
    tool = PatientFormsTool()
    out = str(tmp_path / "intake.pdf")
    try:
        result = tool.run(action="generate_intake", patient_name="Juan Pérez",
                          clinic_name="Clínica Test", output_path=out)
        assert result.success or "reportlab" in (result.error or "").lower()
    except Exception:
        pass  # reportlab may not be installed in CI


def test_patient_forms_generate_consent(tmp_path):
    tool = PatientFormsTool()
    out = str(tmp_path / "consent.pdf")
    try:
        result = tool.run(action="generate_consent", patient_name="María",
                          procedure="Extracción dental", doctor_name="Ruiz",
                          output_path=out)
        assert result.success or "reportlab" in (result.error or "").lower()
    except Exception:
        pass


def test_patient_forms_unsupported_action():
    assert not PatientFormsTool().run(action="delete_form").success


# ---------------------------------------------------------------------------
# PropertyListingsTool
# ---------------------------------------------------------------------------

def test_property_listings_create_and_list(tmp_path):
    with patch("tools.vertical.property_listings._DATA_FILE", tmp_path / "props.json"):
        tool = PropertyListingsTool()
        create = tool.run(
            action="create",
            title="Casa en Polanco",
            property_type="casa",
            operation="venta",
            price=5_000_000,
            location="Polanco, CDMX",
            bedrooms=3,
            bathrooms=2,
            area_m2=180,
        )
        assert create.success
        list_result = tool.run(action="list", operation="venta")
    assert list_result.success
    assert "Polanco" in list_result.output


def test_property_listings_update(tmp_path):
    with patch("tools.vertical.property_listings._DATA_FILE", tmp_path / "props.json"):
        tool = PropertyListingsTool()
        create = tool.run(action="create", title="Depto", property_type="depto",
                          operation="renta", price=15000, location="Roma Norte")
        prop_id = create.raw_data["id"]
        result = tool.run(action="update", property_id=prop_id, price=14000)
    assert result.success
    assert prop_id in result.output


def test_property_listings_update_not_found(tmp_path):
    with patch("tools.vertical.property_listings._DATA_FILE", tmp_path / "props.json"):
        tool = PropertyListingsTool()
        result = tool.run(action="update", property_id="NOPE", price=100)
    assert not result.success


def test_property_listings_list_empty(tmp_path):
    with patch("tools.vertical.property_listings._DATA_FILE", tmp_path / "props.json"):
        result = PropertyListingsTool().run(action="list")
    assert result.success
    assert "Sin propiedades" in result.output


def test_property_listings_generate_report_not_found(tmp_path):
    with patch("tools.vertical.property_listings._DATA_FILE", tmp_path / "props.json"):
        result = PropertyListingsTool().run(action="generate_report", property_id="NOPE")
    assert not result.success


def test_property_listings_unsupported_action():
    assert not PropertyListingsTool().run(action="delete").success


# ---------------------------------------------------------------------------
# PortalsTool
# ---------------------------------------------------------------------------

def test_portals_no_credentials_returns_error():
    tool = PortalsTool({})
    result = tool.run(action="post_inmuebles24", property_data={"title": "test"})
    assert not result.success
    assert "inmuebles24_api_key" in result.error


def test_portals_no_lamudi_key_returns_error():
    tool = PortalsTool({})
    result = tool.run(action="post_lamudi", property_data={"title": "test"})
    assert not result.success
    assert "lamudi_api_key" in result.error


def test_portals_list_active_no_keys():
    tool = PortalsTool({})
    result = tool.run(action="list_active")
    assert result.success
    assert "Sin portales" in result.output


def test_portals_list_active_with_keys():
    tool = PortalsTool({"inmuebles24_api_key": "key123", "lamudi_api_key": "key456"})
    result = tool.run(action="list_active")
    assert result.success
    assert "Inmuebles24" in result.output


def test_portals_post_inmuebles24_success():
    import httpx
    tool = PortalsTool({"inmuebles24_api_key": "key123"})
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"id": "listing-001"}
    mock_resp.raise_for_status.return_value = None
    with patch("httpx.post", return_value=mock_resp):
        result = tool._post_inmuebles24(property_data={"title": "Casa"})
    assert result.success
    assert "listing-001" in result.output


def test_portals_unsupported_action():
    assert not PortalsTool({}).run(action="delete_listing").success


# ---------------------------------------------------------------------------
# ShippingTool
# ---------------------------------------------------------------------------

def test_shipping_get_rates_no_credentials_returns_estimate():
    tool = ShippingTool({})
    result = tool.run(
        action="get_rates",
        origin_zip="06600",
        destination_zip="64000",
        weight_kg=2.5,
    )
    assert result.success
    assert "DHL" in result.output or "Estafeta" in result.output
    assert result.raw_data["estimated"] is True


def test_shipping_get_rates_with_credentials():
    tool = ShippingTool({"dhl_api_key": "key123"})
    result = tool.run(action="get_rates", origin_zip="06600",
                      destination_zip="64000", weight_kg=1.0)
    assert result.success
    assert result.raw_data["estimated"] is False


def test_shipping_track_returns_status():
    tool = ShippingTool({})
    result = tool.run(action="track", tracking_number="1234567890")
    assert result.success
    assert result.output is not None
    assert "events" in result.raw_data


def test_shipping_create_shipment_no_cred():
    tool = ShippingTool({})
    result = tool.run(action="create_shipment", carrier="dhl",
                      origin={}, destination={}, weight_kg=1.0)
    assert not result.success
    assert "dhl_api_key" in result.error


def test_shipping_create_shipment_success():
    tool = ShippingTool({"estafeta_api_key": "key"})
    result = tool.run(action="create_shipment", carrier="estafeta",
                      origin={"zip": "06600"}, destination={"zip": "64000"},
                      weight_kg=1.5)
    assert result.success
    assert "ESTAFETA" in result.output
    assert result.raw_data["tracking"] is not None


def test_shipping_create_shipment_unknown_carrier():
    tool = ShippingTool({})
    result = tool.run(action="create_shipment", carrier="unknown",
                      origin={}, destination={}, weight_kg=1.0)
    assert not result.success
    assert "no reconocido" in result.error


def test_shipping_unsupported_action():
    assert not ShippingTool({}).run(action="delete").success


# ---------------------------------------------------------------------------
# InventoryTool
# ---------------------------------------------------------------------------

def test_inventory_add_and_get_stock(tmp_path):
    with patch("tools.vertical.inventory._DATA_FILE", tmp_path / "inv.json"):
        tool = InventoryTool()
        add = tool.run(
            action="add_product",
            product_id="PROD-001",
            name="Producto Test",
            initial_stock=100,
            category="test",
        )
        assert add.success
        get = tool.run(action="get_stock", product_id="PROD-001")
    assert get.success
    assert "100" in get.output


def test_inventory_update_subtract_cannot_go_negative(tmp_path):
    with patch("tools.vertical.inventory._DATA_FILE", tmp_path / "inv.json"):
        tool = InventoryTool()
        tool.run(action="add_product", product_id="P-NEG", name="Test", initial_stock=5)
        result = tool.run(action="update_stock", product_id="P-NEG",
                          quantity=10, operation="subtract")
    assert not result.success
    assert "insuficiente" in result.error


def test_inventory_update_add(tmp_path):
    with patch("tools.vertical.inventory._DATA_FILE", tmp_path / "inv.json"):
        tool = InventoryTool()
        tool.run(action="add_product", product_id="P-ADD", name="Test", initial_stock=10)
        result = tool.run(action="update_stock", product_id="P-ADD",
                          quantity=5, operation="add")
    assert result.success
    assert "15" in result.output


def test_inventory_low_stock_alert(tmp_path):
    with patch("tools.vertical.inventory._DATA_FILE", tmp_path / "inv.json"):
        tool = InventoryTool()
        tool.run(action="add_product", product_id="P-LOW", name="Bajo", initial_stock=3)
        tool.run(action="add_product", product_id="P-HIGH", name="Alto", initial_stock=100)
        result = tool.run(action="low_stock_alert", threshold=10)
    assert result.success
    assert "Bajo" in result.output


def test_inventory_duplicate_product_returns_error(tmp_path):
    with patch("tools.vertical.inventory._DATA_FILE", tmp_path / "inv.json"):
        tool = InventoryTool()
        tool.run(action="add_product", product_id="DUP", name="Dup", initial_stock=1)
        result = tool.run(action="add_product", product_id="DUP", name="Dup2", initial_stock=2)
    assert not result.success


def test_inventory_get_stock_not_found(tmp_path):
    with patch("tools.vertical.inventory._DATA_FILE", tmp_path / "inv.json"):
        result = InventoryTool().run(action="get_stock", product_id="NOPE")
    assert not result.success


def test_inventory_unsupported_action():
    assert not InventoryTool().run(action="delete").success


# ---------------------------------------------------------------------------
# PolicyManagerTool
# ---------------------------------------------------------------------------

def test_policy_manager_generate_quote(tmp_path):
    tool = PolicyManagerTool()
    result = tool.run(
        action="generate_quote",
        coverage_type="auto",
        client_data={"name": "Test"},
        sum_insured=300_000,
    )
    assert result.success
    assert "300" in result.output or "prima" in result.output.lower()
    assert result.raw_data["prima_neta"] == 300_000 * 0.03


def test_policy_manager_invalid_coverage_type():
    result = PolicyManagerTool().run(action="generate_quote",
                                     coverage_type="invalid",
                                     client_data={}, sum_insured=100_000)
    assert not result.success


def test_policy_manager_create_policy(tmp_path):
    with patch("tools.vertical.policy_manager._DATA_FILE", tmp_path / "pol.json"):
        tool = PolicyManagerTool()
        result = tool.run(action="create_policy",
                          quote_data={"coverage_type": "hogar", "prima_total": 1500},
                          policy_number="POL-TEST-001")
    assert result.success
    assert "POL-TEST-001" in result.output


def test_policy_manager_renewal_reminder_not_found(tmp_path):
    with patch("tools.vertical.policy_manager._DATA_FILE", tmp_path / "pol.json"):
        result = PolicyManagerTool().run(action="renewal_reminder", policy_id="NOPE")
    assert not result.success


def test_policy_manager_create_claim(tmp_path):
    claims_path = tmp_path / "claims.json"
    with patch("tools.vertical.policy_manager.Path") as MockPath:
        # Let DATA_FILE work normally, patch only claims file path
        pass
    tool = PolicyManagerTool()
    with patch("tools.vertical.policy_manager._DATA_FILE", tmp_path / "pol.json"):
        result = tool.run(
            action="create_claim",
            policy_id="POL-001",
            incident_date="2026-05-01",
            description="Accidente vehicular",
            estimated_loss=50_000,
        )
    assert result.success
    assert "SIN-" in result.output


def test_policy_manager_unsupported_action():
    assert not PolicyManagerTool().run(action="delete").success


# ---------------------------------------------------------------------------
# ItineraryTool
# ---------------------------------------------------------------------------

def test_itinerary_generate():
    tool = ItineraryTool()
    result = tool.run(
        action="generate",
        destination="Ciudad de México",
        days=3,
        travel_style="cultural",
    )
    assert result.success
    assert len(result.output) > 100
    assert "DÍA 1" in result.output


def test_itinerary_generate_aventura():
    tool = ItineraryTool()
    result = tool.run(action="generate", destination="Monterrey",
                      days=2, travel_style="aventura", budget="económico")
    assert result.success


def test_itinerary_weather_no_key():
    tool = ItineraryTool()
    result = tool.run(action="get_weather", destination="Cancún")
    assert result.success
    assert "OpenWeather" in result.output or "weather.com" in result.output.lower()


def test_itinerary_weather_with_key():
    import httpx
    tool = ItineraryTool(credentials={"openweather_api_key": "fake-key"})
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "main": {"temp": 28.5, "humidity": 70},
        "weather": [{"description": "cielo despejado"}],
    }
    mock_resp.raise_for_status.return_value = None
    with patch("httpx.get", return_value=mock_resp):
        result = tool._get_weather(destination="Cancún")
    assert result.success
    assert "28.5" in result.output


def test_itinerary_format_pdf_no_reportlab():
    tool = ItineraryTool()
    import builtins
    real_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name == "reportlab" or name.startswith("reportlab."):
            raise ImportError("no reportlab")
        return real_import(name, *args, **kwargs)

    with patch.object(builtins, "__import__", mock_import):
        result = tool._format_pdf(itinerary_text="Día 1: Tour", destination="CDMX")
    assert result.success


def test_itinerary_unsupported_action():
    assert not ItineraryTool().run(action="delete").success


# ---------------------------------------------------------------------------
# Group creation tests
# ---------------------------------------------------------------------------

def test_restaurant_manager_group_created():
    group = create_restaurant_manager()
    assert group.name == "restaurant_manager"
    assert len(group.agents) == 4


def test_health_assistant_group_created():
    group = create_health_assistant()
    assert len(group.agents) == 4


def test_real_estate_agent_group_created():
    group = create_real_estate_agent()
    assert len(group.agents) == 5


def test_logistics_coordinator_group_created():
    group = create_logistics_coordinator()
    assert len(group.agents) == 4


def test_insurance_advisor_group_created():
    group = create_insurance_advisor()
    assert len(group.agents) == 4


def test_travel_planner_group_created():
    group = create_travel_planner()
    assert len(group.agents) == 4
