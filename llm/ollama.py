import httpx
import ollama as ollama_client

from config.settings import settings
from llm.base import BaseLLM, LLMUnavailableError


class OllamaLLM(BaseLLM):
    provider_name = "ollama"

    def __init__(self, host: str = None, model: str = None):
        self.host = host or settings.OLLAMA_HOST
        self.model = model or settings.OLLAMA_MODEL

    def is_available(self) -> bool:
        try:
            response = httpx.get(f"{self.host}/api/tags", timeout=3.0)
            return response.status_code == 200
        except Exception:
            return False

    def generate(self, system_prompt: str, user_message: str) -> str:
        try:
            client = ollama_client.Client(host=self.host)
            response = client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )
            return response.message.content
        except Exception as e:
            raise LLMUnavailableError(
                f"Ollama no disponible en {self.host} con modelo {self.model}: {e}"
            )

    def list_models(self) -> list[str]:
        try:
            client = ollama_client.Client(host=self.host)
            result = client.list()
            return [m.model for m in result.models]
        except Exception:
            return []
