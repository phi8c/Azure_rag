from typing import Any

from openai import AsyncAzureOpenAI

from app.core.settings import settings


class AzureOpenAIService:

    def __init__(self) -> None:

        self._client = AsyncAzureOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT.strip(),
            api_key=settings.AZURE_OPENAI_API_KEY.strip(),
            api_version=settings.AZURE_OPENAI_API_VERSION.strip(),
        )

    async def chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
        temperature: float = 0.2,
        max_completion_tokens: int = 2000,
    ) -> str:
        
        
        print(messages)

        response = await self._client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_completion_tokens
        )

        return (
            response
            .choices[0]
            .message.content
            or ""
        )
        
    async def generate(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.0,
    ) -> str:

        response = await self._client.chat.completions.create(

            model=model,

            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],

            temperature=temperature,

        )

        return (
            response
            .choices[0]
            .message.content
            or ""
        )