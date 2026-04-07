from core.agent import BaseAgent
from core.group import AgentGroup


def create_content_pipeline(db=None) -> AgentGroup:
    agents = [
        BaseAgent("researcher", task_type="long_doc"),
        BaseAgent("writer", task_type="general"),
        BaseAgent("seo_optimizer", task_type="simple"),
        BaseAgent("reviewer", task_type="general"),
    ]
    return AgentGroup("content_pipeline", agents, mode="pipeline", db=db)
