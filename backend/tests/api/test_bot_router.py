import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi import HTTPException

from app.api.v1 import bot_router
from app.enums.prompt_code import PromptCode


class StatelessBotTest(unittest.IsolatedAsyncioTestCase):
    async def test_missing_model_is_rejected_before_external_calls(self):
        with patch.object(bot_router.httpx, "AsyncClient") as client:
            with self.assertRaises(HTTPException) as error:
                await bot_router.teams_message({"text": "Hello"}, db=MagicMock())
        self.assertEqual(error.exception.status_code, 400)
        client.assert_not_called()

    async def test_bot_uses_acl_retrieval_without_database_writes(self):
        db = MagicMock()
        rag = MagicMock()
        rag.load_chat_config = AsyncMock(return_value={})
        rag.ask = AsyncMock(return_value="KNIC answer")
        client = MagicMock()
        client.post = AsyncMock()
        # Exercise Graph pagination and ensure IDs, rather than display names,
        # are passed to the existing ACL-aware retrieval.
        first = MagicMock()
        first.json.return_value = {
            "value": [{"id": "group-1"}],
            "@odata.nextLink": "https://graph.microsoft.com/v1.0/next",
        }
        second = MagicMock()
        second.json.return_value = {"value": [{"id": "group-2"}]}
        client.get = AsyncMock(side_effect=[first, second])
        body = {
            "text": "KNIC?", "from": {"aadObjectId": "user-1"},
            "channelData": {"model_id": "model-1"},
            "conversation": {"id": "teams-thread"},
            "serviceUrl": "https://teams.example/",
        }
        with (
            patch.object(bot_router, "RagService", return_value=rag),
            patch.object(bot_router, "get_token", new=AsyncMock(return_value="token")),
            patch.object(bot_router.httpx, "AsyncClient") as factory,
            patch.object(bot_router.AzureSearchService, "retrieve", new=AsyncMock(return_value=[])) as retrieve,
            patch.object(bot_router.ChatConfigCache, "get_top_k", new=AsyncMock(return_value=7)),
        ):
            factory.return_value.__aenter__.return_value = client
            result = await bot_router.teams_message(body, db=db)
        retrieve.assert_awaited_once_with(
            question="KNIC?", top_k=7, user_object_id="user-1",
            group_ids=["group-1", "group-2"],
        )
        rag.ask.assert_awaited_once_with(
            db=db, question="KNIC?", chunks=[], model_id="model-1",
            mode=PromptCode.INTERNAL, workspace_code=PromptCode.CHAT_RAG.value,
        )
        self.assertEqual(result["text"], "KNIC answer")
        self.assertEqual(db.mock_calls, [])
        client.post.assert_awaited_once()
