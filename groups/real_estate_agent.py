from core.agent import BaseAgent
from core.group import AgentGroup
from tools.vertical.property_listings import PropertyListingsTool
from tools.vertical.portals import PortalsTool
from tools.media.image_resize import ImageResizeTool


def create_real_estate_agent(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    portal_tools = [PortalsTool(creds.get("portals", {}))]

    comm_tools = []
    if creds.get("whatsapp"):
        from tools.crm.whatsapp import WhatsAppTool
        comm_tools.append(WhatsAppTool(creds["whatsapp"]))

    agents = [
        BaseAgent("property_analyst", task_type="reasoning",
                  tools=[PropertyListingsTool()]),
        BaseAgent("listing_writer", task_type="general", tools=[]),
        BaseAgent("image_processor", task_type="simple",
                  tools=[ImageResizeTool()]),
        BaseAgent("portal_publisher", task_type="general",
                  tools=portal_tools),
        BaseAgent("lead_follower", task_type="general",
                  tools=comm_tools),
    ]
    return AgentGroup("real_estate_agent", agents, mode="pipeline", db=db)
