from core.agent import BaseAgent
from core.group import AgentGroup
from tools.social.instagram import InstagramTool
from tools.social.facebook import FacebookTool
from tools.social.linkedin import LinkedInTool
from tools.social.tiktok import TikTokTool
from tools.social.twitter import TwitterTool
from tools.media.image_gen_local import LocalImageGenTool
from tools.media.image_gen_api import APIImageGenTool


def create_social_media_manager(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    social_tools = []
    if creds.get("instagram"):
        social_tools.append(InstagramTool(creds["instagram"]))
    if creds.get("facebook"):
        social_tools.append(FacebookTool(creds["facebook"]))
    if creds.get("linkedin"):
        social_tools.append(LinkedInTool(creds["linkedin"]))
    if creds.get("tiktok"):
        social_tools.append(TikTokTool(creds["tiktok"]))
    if creds.get("twitter"):
        social_tools.append(TwitterTool(creds["twitter"]))

    media_tools = []
    if creds.get("image_gen_local"):
        media_tools.append(LocalImageGenTool(creds["image_gen_local"]))
    if creds.get("image_gen_api"):
        media_tools.append(APIImageGenTool(creds["image_gen_api"]))

    agents = [
        BaseAgent("content_strategist", task_type="reasoning", tools=[]),
        BaseAgent("copywriter", task_type="general", tools=[]),
        BaseAgent("visual_creator", task_type="general", tools=media_tools),
        BaseAgent("social_publisher", task_type="general", tools=social_tools),
        BaseAgent("analytics_reviewer", task_type="simple", tools=social_tools),
    ]
    return AgentGroup("social_media_manager", agents, mode="pipeline", db=db)
