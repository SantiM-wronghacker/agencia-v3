from core.agent import BaseAgent
from core.group import AgentGroup
from tools.vertical.appointment_scheduler import AppointmentSchedulerTool
from tools.vertical.patient_forms import PatientFormsTool


def create_health_assistant(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    comm_tools = []
    if creds.get("whatsapp"):
        from tools.crm.whatsapp import WhatsAppTool
        comm_tools.append(WhatsAppTool(creds["whatsapp"]))
    if creds.get("smtp"):
        from tools.email.smtp import SMTPTool
        comm_tools.append(SMTPTool(creds["smtp"]))

    agents = [
        BaseAgent("appointment_manager", task_type="general",
                  tools=[AppointmentSchedulerTool(creds.get("scheduler", {}))]),
        BaseAgent("patient_communicator", task_type="general",
                  tools=comm_tools),
        BaseAgent("reminder_sender", task_type="simple",
                  tools=[AppointmentSchedulerTool(creds.get("scheduler", {}))] + comm_tools),
        BaseAgent("health_reporter", task_type="general",
                  tools=[PatientFormsTool()]),
    ]
    return AgentGroup("health_assistant", agents, mode="pipeline", db=db)
