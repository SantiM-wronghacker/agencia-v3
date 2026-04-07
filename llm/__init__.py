from config.settings import settings
from llm.base import BaseLLM, LLMUnavailableError
from llm.gemini import GeminiLLM
from llm.groq import GroqLLM
from llm.mistral import MistralLLM
from llm.ollama import OllamaLLM


def _first_available(*providers: BaseLLM) -> BaseLLM:
    for provider in providers:
        if provider.is_available():
            return provider
    raise LLMUnavailableError(
        "No hay ningún proveedor LLM disponible.\n"
        "Verifica que Ollama esté corriendo o configura una API key en .env"
    )


def get_llm(task_type: str = "general") -> BaseLLM:
    provider = settings.LLM_PROVIDER.lower()

    if provider == "ollama":
        return OllamaLLM()
    if provider == "groq":
        return GroqLLM()
    if provider == "gemini":
        return GeminiLLM()
    if provider == "mistral":
        return MistralLLM()

    # auto
    ollama = OllamaLLM()
    groq = GroqLLM()
    gemini = GeminiLLM()
    mistral = MistralLLM()

    if task_type == "reasoning":
        return _first_available(groq, ollama)
    if task_type == "long_doc":
        return _first_available(gemini, groq, ollama)
    if task_type == "simple":
        return _first_available(mistral, ollama)
    # general (default)
    return _first_available(groq, mistral, ollama)
