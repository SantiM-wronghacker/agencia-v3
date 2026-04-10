from core.agent import BaseAgent
from core.group import AgentGroup
from tools.intelligence.web_search import WebSearchTool
from tools.intelligence.web_scraper import WebScraperTool
from tools.intelligence.competitor_analyzer import CompetitorAnalyzerTool
from tools.intelligence.market_data import MarketDataTool


def create_market_intelligence(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    search = WebSearchTool(creds.get("search", {}))
    scraper = WebScraperTool(creds.get("scraper", {}))
    competitor = CompetitorAnalyzerTool(creds.get("competitor", {}))
    market = MarketDataTool(creds.get("market", {}))

    agents = [
        BaseAgent("data_collector", task_type="general",
                  tools=[search, scraper, market]),
        BaseAgent("competitor_analyzer", task_type="reasoning",
                  tools=[competitor, scraper]),
        BaseAgent("trend_identifier", task_type="reasoning",
                  tools=[market, search]),
        BaseAgent("strategic_reporter", task_type="long_doc",
                  tools=[search, market]),
    ]
    return AgentGroup("market_intelligence", agents, mode="pipeline", db=db)
