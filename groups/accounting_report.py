from core.agent import BaseAgent
from core.group import AgentGroup
from tools.accounting.sat_mexico import SATMexicoTool
from tools.accounting.excel_reports import ExcelReportsTool
from tools.accounting.csv_processor import CSVProcessorTool
from tools.documents.pdf_generator import PDFGeneratorTool


def create_accounting_report(db=None, credentials: dict = None) -> AgentGroup:
    agents = [
        BaseAgent("data_collector", task_type="general",
                  tools=[CSVProcessorTool(), ExcelReportsTool()]),
        BaseAgent("accounting_analyst", task_type="reasoning",
                  tools=[SATMexicoTool()]),
        BaseAgent("tax_calculator", task_type="reasoning",
                  tools=[SATMexicoTool()]),
        BaseAgent("report_generator", task_type="general",
                  tools=[ExcelReportsTool(), PDFGeneratorTool()]),
    ]
    return AgentGroup("accounting_report", agents, mode="pipeline", db=db)
