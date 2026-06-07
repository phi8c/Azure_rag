from app.services.llm.ollama_service import (
    OllamaService
)


class LLMFactory:

    @staticmethod
    def get_llm():

        return OllamaService()