from core.agent import BaseAgent
from core.group import AgentGroup
from tools.vertical.itinerary import ItineraryTool


def create_travel_planner(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    comm_tools = []
    if creds.get("whatsapp"):
        from tools.crm.whatsapp import WhatsAppTool
        comm_tools.append(WhatsAppTool(creds["whatsapp"]))
    if creds.get("smtp"):
        from tools.email.smtp import SMTPTool
        comm_tools.append(SMTPTool(creds["smtp"]))

    itinerary = ItineraryTool(creds.get("itinerary", {}))

    agents = [
        BaseAgent("destination_researcher", task_type="long_doc",
                  tools=[itinerary]),
        BaseAgent("itinerary_creator", task_type="general",
                  tools=[itinerary]),
        BaseAgent("budget_calculator", task_type="reasoning",
                  tools=[]),
        BaseAgent("package_presenter", task_type="general",
                  tools=[itinerary] + comm_tools),
    ]
    return AgentGroup("travel_planner", agents, mode="pipeline", db=db)
