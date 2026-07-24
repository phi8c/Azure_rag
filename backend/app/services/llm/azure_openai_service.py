import json
from typing import Any

from openai import AsyncAzureOpenAI

from app.core.settings import settings


class AzureOpenAIService:
    """
    Azure OpenAI chat service.

    Notes:
    - model must be the Azure Deployment Name.
    - It is recommended to keep the deployment name identical to the model name
      (e.g. gpt-5.1, gpt-5.2).
    """

    def __init__(self) -> None:
        
        
        
        print("========== AZURE CONFIG ==========")
        print("ENDPOINT :", repr(settings.AZURE_OPENAI_ENDPOINT))
        print("VERSION  :", repr(settings.AZURE_OPENAI_API_VERSION))
        print("KEY      :", repr(settings.AZURE_OPENAI_API_KEY[:10]))
        print("==================================")

        self._client = AsyncAzureOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT.strip(),
            api_key=settings.AZURE_OPENAI_API_KEY.strip(),
            api_version=settings.AZURE_OPENAI_API_VERSION.strip(),
        )
        print(repr(settings.AZURE_OPENAI_ENDPOINT))
        print(repr(settings.AZURE_OPENAI_API_VERSION))
        print(repr(settings.AZURE_OPENAI_API_KEY[:10]))

    async def chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        """
        Send chat completion request.

        Args:
            model:
                Azure deployment name.

            messages:
                OpenAI chat messages.

            temperature:
                Sampling temperature.

        Returns:
            Parsed JSON response.
        """
        
        print("ENDPOINT:", repr(settings.AZURE_OPENAI_ENDPOINT))
        print("API_VERSION:", repr(settings.AZURE_OPENAI_API_VERSION))
        print("MODEL:", repr(model))

        response = await self._client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        
        print("MODEL:", repr(model))

        content = (
            response
            .choices[0]
            .message.content
            or "{}"
        )

        try:
            return json.loads(content)

        except json.JSONDecodeError as ex:
            raise ValueError(
                "Azure OpenAI returned invalid JSON."
            ) from ex