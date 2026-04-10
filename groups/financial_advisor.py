from core.agent import BaseAgent
from core.group import AgentGroup
from tools.intelligence.market_data import MarketDataTool
from tools.intelligence.financial_calculator import FinancialCalculatorTool
from tools.intelligence.banxico import BanxicoTool


def create_financial_advisor(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    market = MarketDataTool(creds.get("market", {}))
    calculator = FinancialCalculatorTool(creds.get("calculator", {}))
    banxico = BanxicoTool(creds.get("banxico", {}))

    agents = [
        BaseAgent("data_gatherer", task_type="general",
                  tools=[market, banxico]),
        BaseAgent("financial_analyst", task_type="reasoning",
                  tools=[calculator, market, banxico]),
        BaseAgent("risk_evaluator", task_type="reasoning",
                  tools=[calculator, banxico]),
        BaseAgent("recommendation_writer", task_type="long_doc",
                  tools=[calculator]),
    ]
    return AgentGroup("financial_advisor", agents, mode="pipeline", db=db)
