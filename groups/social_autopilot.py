from core.agent import BaseAgent
from core.group import AgentGroup
from tools.intelligence.web_search import WebSearchTool
from tools.media.image_gen_local import LocalImageGenTool
from tools.media.image_resize import ImageResizeTool


def create_social_autopilot(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    search_tools = [WebSearchTool(creds.get("search", {}))]

    social_tools = []
    if creds.get("instagram"):
        from tools.social.instagram import InstagramTool
        social_tools.append(InstagramTool(creds["instagram"]))
    if creds.get("facebook"):
        from tools.social.facebook import FacebookTool
        social_tools.append(FacebookTool(creds["facebook"]))
    if creds.get("linkedin"):
        from tools.social.linkedin import LinkedInTool
        social_tools.append(LinkedInTool(creds["linkedin"]))
    if creds.get("twitter"):
        from tools.social.twitter import TwitterTool
        social_tools.append(TwitterTool(creds["twitter"]))

    agents = [
        BaseAgent("topic_selector", task_type="reasoning",
                  tools=search_tools),
        BaseAgent("content_creator", task_type="general", tools=[]),
        BaseAgent("image_generator", task_type="simple",
                  tools=[LocalImageGenTool(), ImageResizeTool()]),
        BaseAgent("auto_publisher", task_type="general",
                  tools=social_tools),
    ]
    return AgentGroup("social_autopilot", agents, mode="pipeline", db=db)
