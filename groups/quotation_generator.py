from core.agent import BaseAgent
from core.group import AgentGroup
from tools.crm.whatsapp import WhatsAppTool
from tools.email.smtp import SMTPTool
from tools.documents.pdf_generator import PDFGeneratorTool


def create_quotation_generator(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    comm_tools = []
    if creds.get("whatsapp"):
        comm_tools.append(WhatsAppTool(creds["whatsapp"]))
    if creds.get("smtp"):
        comm_tools.append(SMTPTool(creds["smtp"]))

    agents = [
        BaseAgent("requirements_analyst", task_type="reasoning", tools=[]),
        BaseAgent("pricing_calculator", task_type="reasoning", tools=[]),
        BaseAgent("proposal_writer", task_type="general", tools=[PDFGeneratorTool()]),
        BaseAgent("quotation_sender", task_type="general", tools=comm_tools),
    ]
    return AgentGroup("quotation_generator", agents, mode="pipeline", db=db)
