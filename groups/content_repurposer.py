from core.agent import BaseAgent
from core.group import AgentGroup
from tools.social.instagram import InstagramTool
from tools.social.linkedin import LinkedInTool
from tools.social.twitter import TwitterTool
from tools.web.wordpress import WordPressTool
from tools.web.ghost import GhostTool
from tools.media.image_resize import ImageResizeTool
from tools.documents.pdf_generator import PDFGeneratorTool


def create_content_repurposer(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    social_tools = []
    if creds.get("instagram"):
        social_tools.append(InstagramTool(creds["instagram"]))
    if creds.get("linkedin"):
        social_tools.append(LinkedInTool(creds["linkedin"]))
    if creds.get("twitter"):
        social_tools.append(TwitterTool(creds["twitter"]))

    publish_tools = []
    if creds.get("wordpress"):
        publish_tools.append(WordPressTool(creds["wordpress"]))
    if creds.get("ghost"):
        publish_tools.append(GhostTool(creds["ghost"]))

    media_tools = []
    if creds.get("image_resize"):
        media_tools.append(ImageResizeTool(creds["image_resize"]))

    doc_tools = []
    if creds.get("pdf"):
        doc_tools.append(PDFGeneratorTool(creds["pdf"]))

    agents = [
        BaseAgent("content_analyzer", task_type="reasoning", tools=[]),
        BaseAgent("social_adapter", task_type="general", tools=social_tools),
        BaseAgent("blog_adapter", task_type="general", tools=publish_tools),
        BaseAgent("visual_adapter", task_type="general", tools=media_tools),
        BaseAgent("distribution_manager", task_type="simple", tools=social_tools + publish_tools),
    ]
    return AgentGroup("content_repurposer", agents, mode="parallel", db=db)
