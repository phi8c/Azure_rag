from typing import Any, AsyncIterator

from openai import AsyncAzureOpenAI
from anthropic import AsyncAnthropic

from app.core.settings import settings


class LLMResponseTruncatedError(ValueError):
    pass


class AzureOpenAIService:

    def __init__(self) -> None:
        self._client = None
        if (
            settings.AZURE_OPENAI_ENDPOINT
            and settings.AZURE_OPENAI_API_KEY
            and settings.AZURE_OPENAI_API_VERSION
        ):
            self._client = AsyncAzureOpenAI(
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT.strip(),
                api_key=settings.AZURE_OPENAI_API_KEY.strip(),
                api_version=settings.AZURE_OPENAI_API_VERSION.strip(),
            )
        self._claude_client = None
        if settings.CLAUDE_API_KEY.strip():
            default_headers = {}
            if settings.CLAUDE_WORKSPACE_ID.strip():
                default_headers["anthropic-workspace-id"] = (
                    settings.CLAUDE_WORKSPACE_ID.strip()
                )
            self._claude_client = AsyncAnthropic(
                api_key=settings.CLAUDE_API_KEY.strip(),
                default_headers=default_headers or None,
            )

    @staticmethod
    def _is_claude(model: str, provider: str | None = None) -> bool:
        return (
            (provider is not None and provider.lower() in {"anthropic", "claude"})
            or model.startswith("claude-")
        )

    def _get_claude_client(self) -> AsyncAnthropic:
        if self._claude_client is None:
            raise RuntimeError("CLAUDE_API_KEY is required to use Claude models.")
        return self._claude_client

    def _get_azure_client(self) -> AsyncAzureOpenAI:
        if self._client is None:
            raise RuntimeError("Azure OpenAI settings are required to use Azure models.")
        return self._client

    @staticmethod
    def _claude_messages(
        messages: list[dict[str, Any]],
    ) -> tuple[str, list[dict[str, Any]]]:
        system = "\n\n".join(
            str(message.get("content", ""))
            for message in messages
            if message.get("role") == "system"
        )
        claude_messages = [
            {"role": message["role"], "content": message.get("content", "")}
            for message in messages
            if message.get("role") in {"user", "assistant"}
        ]
        return system, claude_messages

    async def chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
        temperature: float = 0.2,
        max_completion_tokens: int = 2000,
        provider: str | None = None,
    ) -> str:
        if self._is_claude(model, provider):
            system, claude_messages = self._claude_messages(messages)
            response = await self._get_claude_client().messages.create(
                model=model,
                system=system or "You are a helpful assistant.",
                messages=claude_messages,
                temperature=temperature,
                max_tokens=max_completion_tokens,
            )
            return "".join(
                block.text for block in response.content if block.type == "text"
            )
        
        response = await self._get_azure_client().chat.completions.create(
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

    async def chat_json(
        self,
        model: str,
        messages: list[dict[str, Any]],
        temperature: float = 0.2,
        max_completion_tokens: int = 2000,
        provider: str | None = None,
    ) -> str:

        if self._is_claude(model, provider):
            system, claude_messages = self._claude_messages(messages)
            response = await self._get_claude_client().messages.create(
                model=model,
                system=(system + "\n\nReturn only valid JSON.").strip(),
                messages=claude_messages,
                temperature=temperature,
                max_tokens=max_completion_tokens,
            )
            if response.stop_reason == "max_tokens":
                raise LLMResponseTruncatedError(
                    "LLM JSON response reached the output token limit."
                )
            return "".join(
                block.text for block in response.content if block.type == "text"
            )

        response = await self._get_azure_client().chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_completion_tokens,
            response_format={
                "type": "json_object",
            },
        )

        choice = response.choices[0]

        if choice.finish_reason == "length":
            raise LLMResponseTruncatedError(
                "LLM JSON response reached the output token limit."
            )

        return choice.message.content or ""

    async def chat_stream(
        self,
        model: str,
        messages: list[dict[str, Any]],
        temperature: float = 0.2,
        max_completion_tokens: int = 2000,
        provider: str | None = None,
    ) -> AsyncIterator[str]:

        if self._is_claude(model, provider):
            system, claude_messages = self._claude_messages(messages)
            async with self._get_claude_client().messages.stream(
                model=model,
                system=system or "You are a helpful assistant.",
                messages=claude_messages,
                temperature=temperature,
                max_tokens=max_completion_tokens,
            ) as stream:
                async for text in stream.text_stream:
                    yield text
            return

        stream = await self._get_azure_client().chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_completion_tokens,
            stream=True,
        )

        async for chunk in stream:

            if not chunk.choices:
                continue

            content = (
                chunk
                .choices[0]
                .delta
                .content
            )

            if content:
                yield content
        
    async def generate(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.0,
    ) -> str:

        if self._is_claude(model):
            response = await self._get_claude_client().messages.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=2000,
            )
            return "".join(
                block.text for block in response.content if block.type == "text"
            )

        if self._client is None:
            return prompt

        response = await self._get_azure_client().chat.completions.create(

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


#
# Dùng chung 1 client (connection pool) cho mọi request chat
#

_shared_service: AzureOpenAIService | None = None


def get_shared_azure_openai_service() -> AzureOpenAIService:

    global _shared_service

    if _shared_service is None:

        _shared_service = AzureOpenAIService()

    return _shared_service
