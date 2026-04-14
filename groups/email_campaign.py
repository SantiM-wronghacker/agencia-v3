from core.agent import BaseAgent
from core.group import AgentGroup
from tools.email.smtp import SMTPTool
from tools.email.mailchimp import MailchimpTool
from tools.crm.hubspot import HubSpotTool
from tools.crm.google_sheets import GoogleSheetsTool


def create_email_campaign(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    email_tools = []
    if creds.get("smtp"):
        email_tools.append(SMTPTool(creds["smtp"]))
    if creds.get("mailchimp"):
        email_tools.append(MailchimpTool(creds["mailchimp"]))

    crm_tools = []
    if creds.get("hubspot"):
        crm_tools.append(HubSpotTool(creds["hubspot"]))
    if creds.get("google_sheets"):
        crm_tools.append(GoogleSheetsTool(creds["google_sheets"]))

    agents = [
        BaseAgent("audience_segmenter", task_type="reasoning", tools=crm_tools),
        BaseAgent("copywriter", task_type="general", tools=[]),
        BaseAgent("subject_optimizer", task_type="simple", tools=[]),
        BaseAgent("campaign_sender", task_type="general", tools=email_tools),
        BaseAgent("results_analyst", task_type="simple", tools=email_tools),
    ]
    return AgentGroup("email_campaign", agents, mode="pipeline", db=db)
