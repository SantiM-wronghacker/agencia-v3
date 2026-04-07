from google import genai
from google.genai import types

from config.settings import settings
from llm.base import BaseLLM, LLMUnavailableError


class GeminiLLM(BaseLLM):
    provider_name = "gemini"

    def __init__(self, model: str = "gemini-2.0-flash"):
        self.model = model

    def is_available(self) -> bool:
        return bool(settings.GEMINI_API_KEY)

    def generate(self, system_prompt: str, user_message: str) -> str:
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            response = client.models.generate_content(
                model=self.model,
                contents=user_message,
                config=types.GenerateContentConfig(system_instruction=system_prompt),
            )
            return response.text
        except Exception as e:
            raise LLMUnavailableError(f"Gemini falló con modelo {self.model}: {e}")
