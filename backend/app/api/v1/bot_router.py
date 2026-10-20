"""Teams adapter without database conversations, message storage or query rewriting."""

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.settings import settings
from app.enums.prompt_code import PromptCode
from app.services.azure.azure_search_service import AzureSearchService
from app.services.rag.chat_config_cache import ChatConfigCache
from app.services.rag.rag_service import RagService


router = APIRouter(prefix="/bot", tags=["Bot"])


async def get_token(client: httpx.AsyncClient, client_id: str, secret: str, scope: str):
    response = await client.post(
        f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}/oauth2/v2.0/token",
        data={
            "client_id": client_id, "client_secret": secret,
            "scope": scope, "grant_type": "client_credentials",
        },
    )
    response.raise_for_status()
    return response.json()["access_token"]


@router.post("/messages")
async def teams_message(body: dict, db: AsyncSession = Depends(get_db)):
    question = body.get("text", "").strip()
    object_id = body.get("from", {}).get("aadObjectId")
    model_id = body.get("model_id") or body.get("channelData", {}).get("model_id")
    service_url = body.get("serviceUrl")
    conversation_id = body.get("conversation", {}).get("id")
    if not all((question, object_id, model_id, service_url, conversation_id)):
        raise HTTPException(400, "text, from.aadObjectId, model_id, serviceUrl and conversation.id are required")

    rag = RagService()
    try:
        # Validate configuration before retrieval or sending a Teams reply.
        await rag.load_chat_config(
            db=db, model_id=model_id, mode=PromptCode.INTERNAL,
            workspace_code=PromptCode.CHAT_RAG.value,
        )
    except (ValueError, LookupError) as exc:
        raise HTTPException(400, str(exc)) from exc

    async with httpx.AsyncClient(timeout=30) as client:
        graph_token = await get_token(
            client, settings.AZURE_CLIENT_ID, settings.AZURE_CLIENT_SECRET,
            "https://graph.microsoft.com/.default",
        )
        group_ids = []
        url = f"https://graph.microsoft.com/v1.0/users/{object_id}/transitiveMemberOf/microsoft.graph.group?$select=id"
        while url:
            response = await client.get(url, headers={"Authorization": f"Bearer {graph_token}"})
            response.raise_for_status()
            data = response.json()
            group_ids.extend(group["id"] for group in data.get("value", []))
            url = data.get("@odata.nextLink")

        chunks = await AzureSearchService.retrieve_with_acl(
            question=question,
            top_k=await ChatConfigCache.get_top_k(PromptCode.CHAT_RAG.value) or 10,
            user_object_id=object_id, group_ids=group_ids,
        )
        answer = await rag.ask(
            db=db, question=question,
            chunks=chunks, model_id=model_id, mode=PromptCode.INTERNAL,
            workspace_code=PromptCode.CHAT_RAG.value,
        )
        bot_token = await get_token(
            client, settings.BOT_APP_ID, settings.BOT_APP_SECRET,
            "https://api.botframework.com/.default",
        )
        response = await client.post(
            f"{service_url.rstrip('/')}/v3/conversations/{conversation_id}/activities",
            headers={"Authorization": f"Bearer {bot_token}"},
            json={"type": "message", "text": answer},
        )
        response.raise_for_status()
    return {"type": "message", "text": answer}
