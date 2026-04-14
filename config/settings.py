from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LLM_PROVIDER: str = "auto"

    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral:7b"

    GROQ_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    MISTRAL_API_KEY: str = ""

    DB_PATH: str = "data/agencia.db"
    EXPORT_PATH: str = "export/"
    LICENSE_SERVER_URL: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def llm_provider(self) -> str:
        return self.LLM_PROVIDER

    @property
    def ollama_host(self) -> str:
        return self.OLLAMA_HOST

    @property
    def db_path(self) -> str:
        return self.DB_PATH


settings = Settings()
