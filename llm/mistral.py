from mistralai import Mistral

from config.settings import settings
from llm.base import BaseLLM, LLMUnavailableError


class MistralLLM(BaseLLM):
    provider_name = "mistral"

    def __init__(self, model: str = "mistral-small-latest"):
        self.model = model

    def is_available(self) -> bool:
        return bool(settings.MISTRAL_API_KEY)

    def generate(self, system_prompt: str, user_message: str) -> str:
        try:
            client = Mistral(api_key=settings.MISTRAL_API_KEY)
            response = client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            raise LLMUnavailableError(f"Mistral falló con modelo {self.model}: {e}")
