from core.agent import BaseAgent
from core.group import AgentGroup
from tools.productivity.trello import TrelloTool
from tools.productivity.notion import NotionTool
from tools.productivity.slack import SlackTool
from tools.email.smtp import SMTPTool


def create_ops_daily(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    task_tools = []
    if creds.get("trello"):
        task_tools.append(TrelloTool(creds["trello"]))
    if creds.get("notion"):
        task_tools.append(NotionTool(creds["notion"]))

    comm_tools = []
    if creds.get("slack"):
        comm_tools.append(SlackTool(creds["slack"]))
    if creds.get("smtp"):
        comm_tools.append(SMTPTool(creds["smtp"]))

    agents = [
        BaseAgent("task_reviewer", task_type="general", tools=task_tools),
        BaseAgent("priority_manager", task_type="reasoning", tools=[]),
        BaseAgent("delegator", task_type="general", tools=task_tools),
        BaseAgent("status_reporter", task_type="simple", tools=comm_tools),
    ]
    return AgentGroup("ops_daily", agents, mode="pipeline", db=db)
