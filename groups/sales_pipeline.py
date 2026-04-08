from core.agent import BaseAgent
from core.group import AgentGroup
from tools.crm.hubspot import HubSpotTool
from tools.crm.google_sheets import GoogleSheetsTool
from tools.crm.whatsapp import WhatsAppTool
from tools.documents.pdf_generator import PDFGeneratorTool
from tools.documents.word_generator import WordGeneratorTool


def create_sales_pipeline(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    crm_tools = []
    if creds.get("hubspot"):
        crm_tools.append(HubSpotTool(creds["hubspot"]))
    if creds.get("google_sheets"):
        crm_tools.append(GoogleSheetsTool(creds["google_sheets"]))

    comm_tools = []
    if creds.get("whatsapp"):
        comm_tools.append(WhatsAppTool(creds["whatsapp"]))

    doc_tools = [PDFGeneratorTool(), WordGeneratorTool()]

    agents = [
        BaseAgent("lead_qualifier", task_type="reasoning", tools=crm_tools),
        BaseAgent("proposal_writer", task_type="general", tools=doc_tools),
        BaseAgent("follow_up_manager", task_type="general", tools=comm_tools),
        BaseAgent("closing_agent", task_type="reasoning", tools=crm_tools + comm_tools),
    ]
    return AgentGroup("sales_pipeline", agents, mode="pipeline", db=db)
