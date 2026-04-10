from core.agent import BaseAgent
from core.group import AgentGroup


def create_lead_nurturing(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    crm_tools = []
    if creds.get("hubspot"):
        from tools.crm.hubspot import HubSpotTool
        crm_tools.append(HubSpotTool(creds["hubspot"]))
    if creds.get("google_sheets"):
        from tools.crm.google_sheets import GoogleSheetsTool
        crm_tools.append(GoogleSheetsTool(creds["google_sheets"]))

    comm_tools = []
    if creds.get("whatsapp"):
        from tools.crm.whatsapp import WhatsAppTool
        comm_tools.append(WhatsAppTool(creds["whatsapp"]))
    if creds.get("smtp"):
        from tools.email.smtp import SMTPTool
        comm_tools.append(SMTPTool(creds["smtp"]))

    agents = [
        BaseAgent("lead_qualifier", task_type="reasoning",
                  tools=crm_tools),
        BaseAgent("personalized_writer", task_type="general",
                  tools=[]),
        BaseAgent("message_sender", task_type="general",
                  tools=comm_tools),
        BaseAgent("crm_updater", task_type="simple",
                  tools=crm_tools),
    ]
    return AgentGroup("lead_nurturing", agents, mode="pipeline", db=db)
