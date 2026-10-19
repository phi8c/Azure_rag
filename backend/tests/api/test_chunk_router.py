import unittest
from unittest.mock import patch

from app.api.v1.chunk_router import get_all_chunks, router
from app.api.v1.document_router import sync_completed
from app.services.sync_jobs.sync_state import SyncState


class ReadOnlyChunksTest(unittest.IsolatedAsyncioTestCase):
    async def test_read_chunks_passes_parent_id_to_search(self):
        chunks = [{"id": "chunk-1", "content": "KNIC"}]
        with patch(
            "app.api.v1.chunk_router.AzureChunkRepository.load_chunks",
            return_value=chunks,
        ) as load:
            result = await get_all_chunks(parent_id="document-1")
        load.assert_called_once_with("document-1")
        self.assertEqual(result, {"total": 1, "chunks": chunks})
        self.assertTrue(all(route.methods == {"GET"} for route in router.routes))

    async def test_completion_callback_does_not_touch_chunk_files(self):
        previous_status = SyncState.status
        self.addCleanup(setattr, SyncState, "status", previous_status)
        SyncState.status = "RUNNING"
        with patch("builtins.open", side_effect=AssertionError("Unexpected file access")):
            result = await sync_completed()
        self.assertEqual(result, {"status": "accepted"})
        self.assertEqual(SyncState.status, "COMPLETED")
