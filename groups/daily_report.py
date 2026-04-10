from core.agent import BaseAgent
from core.group import AgentGroup
from tools.accounting.csv_processor import CSVProcessorTool
from tools.accounting.excel_reports import ExcelReportsTool
from tools.intelligence.financial_calculator import FinancialCalculatorTool
from tools.intelligence.banxico import BanxicoTool
from tools.documents.pdf_generator import PDFGeneratorTool


def create_daily_report(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    comm_tools = []
    if creds.get("slack"):
        from tools.productivity.slack import SlackTool
        comm_tools.append(SlackTool(creds["slack"]))
    if creds.get("smtp"):
        from tools.email.smtp import SMTPTool
        comm_tools.append(SMTPTool(creds["smtp"]))

    storage_tools = []
    if creds.get("google_drive"):
        from tools.storage.google_drive import GoogleDriveTool
        storage_tools.append(GoogleDriveTool(creds["google_drive"]))

    agents = [
        BaseAgent("data_collector", task_type="general",
                  tools=[CSVProcessorTool(), ExcelReportsTool()]),
        BaseAgent("daily_analyst", task_type="reasoning",
                  tools=[FinancialCalculatorTool(), BanxicoTool()]),
        BaseAgent("report_writer", task_type="general",
                  tools=[ExcelReportsTool(), PDFGeneratorTool()] + storage_tools),
        BaseAgent("report_distributor", task_type="simple",
                  tools=comm_tools),
    ]
    return AgentGroup("daily_report", agents, mode="pipeline", db=db)
