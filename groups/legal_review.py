from core.agent import BaseAgent
from core.group import AgentGroup


def create_legal_review(db=None) -> AgentGroup:
    agents = [
        BaseAgent("legal_analyst", task_type="long_doc"),
        BaseAgent("compliance_checker", task_type="reasoning"),
        BaseAgent("risk_assessor", task_type="reasoning"),
        BaseAgent("summarizer", task_type="simple"),
    ]
    return AgentGroup("legal_review", agents, mode="pipeline", db=db)
