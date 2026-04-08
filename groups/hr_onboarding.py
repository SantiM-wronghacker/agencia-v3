from core.agent import BaseAgent
from core.group import AgentGroup
from tools.productivity.notion import NotionTool
from tools.productivity.slack import SlackTool
from tools.email.smtp import SMTPTool
from tools.documents.word_generator import WordGeneratorTool
from tools.documents.pdf_generator import PDFGeneratorTool


def create_hr_onboarding(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    comm_tools = []
    if creds.get("slack"):
        comm_tools.append(SlackTool(creds["slack"]))
    if creds.get("smtp"):
        comm_tools.append(SMTPTool(creds["smtp"]))

    doc_tools = [WordGeneratorTool(), PDFGeneratorTool()]

    notion_tools = []
    if creds.get("notion"):
        notion_tools.append(NotionTool(creds["notion"]))

    agents = [
        BaseAgent("profile_analyst", task_type="reasoning", tools=[]),
        BaseAgent("document_generator", task_type="general", tools=doc_tools),
        BaseAgent("orientation_planner", task_type="general", tools=notion_tools),
        BaseAgent("hr_communicator", task_type="general", tools=comm_tools),
    ]
    return AgentGroup("hr_onboarding", agents, mode="pipeline", db=db)
