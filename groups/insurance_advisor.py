from core.agent import BaseAgent
from core.group import AgentGroup
from tools.vertical.policy_manager import PolicyManagerTool


def create_insurance_advisor(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    comm_tools = []
    if creds.get("whatsapp"):
        from tools.crm.whatsapp import WhatsAppTool
        comm_tools.append(WhatsAppTool(creds["whatsapp"]))
    if creds.get("smtp"):
        from tools.email.smtp import SMTPTool
        comm_tools.append(SMTPTool(creds["smtp"]))

    policy = PolicyManagerTool()

    agents = [
        BaseAgent("needs_analyst", task_type="reasoning", tools=[]),
        BaseAgent("quote_generator", task_type="general",
                  tools=[policy]),
        BaseAgent("policy_explainer", task_type="general", tools=[]),
        BaseAgent("renewal_manager", task_type="general",
                  tools=[policy] + comm_tools),
    ]
    return AgentGroup("insurance_advisor", agents, mode="pipeline", db=db)
