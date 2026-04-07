from groq import Groq

from config.settings import settings
from llm.base import BaseLLM, LLMUnavailableError


class GroqLLM(BaseLLM):
    provider_name = "groq"

    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.model = model

    def is_available(self) -> bool:
        return bool(settings.GROQ_API_KEY)

    def generate(self, system_prompt: str, user_message: str) -> str:
        try:
            client = Groq(api_key=settings.GROQ_API_KEY)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            raise LLMUnavailableError(f"Groq falló con modelo {self.model}: {e}")
