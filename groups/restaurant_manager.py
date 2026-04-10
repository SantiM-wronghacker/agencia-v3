from core.agent import BaseAgent
from core.group import AgentGroup
from tools.vertical.menu_manager import MenuManagerTool
from tools.vertical.reservations import ReservationsTool


def create_restaurant_manager(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}
    agents = [
        BaseAgent("menu_analyst", task_type="general",
                  tools=[MenuManagerTool()]),
        BaseAgent("content_creator", task_type="general", tools=[]),
        BaseAgent("review_responder", task_type="reasoning", tools=[]),
        BaseAgent("reservation_manager", task_type="general",
                  tools=[ReservationsTool(creds.get("reservations", {}))]),
    ]
    return AgentGroup("restaurant_manager", agents, mode="pipeline", db=db)
