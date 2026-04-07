from core.agent import BaseAgent
from core.group import AgentGroup


def create_ops_automation(db=None) -> AgentGroup:
    agents = [
        BaseAgent("process_mapper", task_type="general"),
        BaseAgent("optimizer", task_type="reasoning"),
        BaseAgent("implementation_planner", task_type="general"),
    ]
    return AgentGroup("ops_automation", agents, mode="pipeline", db=db)
