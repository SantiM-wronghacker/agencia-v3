from abc import ABC, abstractmethod


class LLMUnavailableError(Exception):
    pass


class BaseLLM(ABC):
    provider_name: str

    @abstractmethod
    def generate(self, system_prompt: str, user_message: str) -> str:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass
