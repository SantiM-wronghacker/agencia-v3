from core.agent import BaseAgent
from core.group import AgentGroup
from tools.intelligence.quiz_generator import QuizGeneratorTool
from tools.intelligence.learning_tracker import LearningTrackerTool


def create_education_manager(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    quiz = QuizGeneratorTool(creds.get("quiz", {}))
    tracker = LearningTrackerTool(creds.get("tracker", {}))

    agents = [
        BaseAgent("curriculum_designer", task_type="long_doc",
                  tools=[tracker]),
        BaseAgent("content_creator", task_type="general",
                  tools=[quiz]),
        BaseAgent("assessment_builder", task_type="reasoning",
                  tools=[quiz]),
        BaseAgent("progress_tracker", task_type="general",
                  tools=[tracker]),
    ]
    return AgentGroup("education_manager", agents, mode="pipeline", db=db)
