from core.agent import BaseAgent
from core.group import AgentGroup
from tools.web.wordpress import WordPressTool
from tools.web.ghost import GhostTool
from tools.web.webflow import WebflowTool
from tools.media.image_gen_local import LocalImageGenTool
from tools.media.image_gen_api import APIImageGenTool
from tools.documents.pdf_generator import PDFGeneratorTool


def create_blog_publisher(db=None, credentials: dict = None) -> AgentGroup:
    creds = credentials or {}

    publish_tools = []
    if creds.get("wordpress"):
        publish_tools.append(WordPressTool(creds["wordpress"]))
    if creds.get("ghost"):
        publish_tools.append(GhostTool(creds["ghost"]))
    if creds.get("webflow"):
        publish_tools.append(WebflowTool(creds["webflow"]))

    media_tools = []
    if creds.get("image_gen_local"):
        media_tools.append(LocalImageGenTool(creds["image_gen_local"]))
    if creds.get("image_gen_api"):
        media_tools.append(APIImageGenTool(creds["image_gen_api"]))

    doc_tools = []
    if creds.get("pdf"):
        doc_tools.append(PDFGeneratorTool(creds["pdf"]))

    agents = [
        BaseAgent("seo_strategist", task_type="reasoning", tools=[]),
        BaseAgent("content_writer", task_type="general", tools=[]),
        BaseAgent("image_creator", task_type="general", tools=media_tools),
        BaseAgent("seo_optimizer", task_type="simple", tools=[]),
        BaseAgent("publisher", task_type="general", tools=publish_tools),
    ]
    return AgentGroup("blog_publisher", agents, mode="pipeline", db=db)
