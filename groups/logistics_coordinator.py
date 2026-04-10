from core.agent import BaseAgent
from core.group import AgentGroup
from tools.vertical.shipping import ShippingTool
from tools.vertical.inventory import InventoryTool


def create_logistics_coordinator(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    comm_tools = []
    if creds.get("whatsapp"):
        from tools.crm.whatsapp import WhatsAppTool
        comm_tools.append(WhatsAppTool(creds["whatsapp"]))

    shipping = ShippingTool(creds.get("shipping", {}))
    inventory = InventoryTool(creds.get("inventory", {}))

    agents = [
        BaseAgent("shipment_planner", task_type="reasoning",
                  tools=[shipping, inventory]),
        BaseAgent("rate_calculator", task_type="simple",
                  tools=[shipping]),
        BaseAgent("tracking_monitor", task_type="general",
                  tools=[shipping]),
        BaseAgent("customer_notifier", task_type="general",
                  tools=comm_tools),
    ]
    return AgentGroup("logistics_coordinator", agents, mode="pipeline", db=db)
