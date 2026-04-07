from core.agent import BaseAgent
from core.group import AgentGroup


def create_business_analysis(db=None) -> AgentGroup:
    agents = [
        BaseAgent("data_analyst", task_type="reasoning"),
        BaseAgent("strategy_director", task_type="reasoning"),
        BaseAgent("finance_director", task_type="reasoning"),
        BaseAgent("reporter", task_type="simple"),
    ]
    return AgentGroup("business_analysis", agents, mode="pipeline", db=db)
