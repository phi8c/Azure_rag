import hashlib
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.contract.contract_service import ContractService
from app.utils.extract.document_intelligent import DocumentExtractor


class AzureDocumentMigrationTest(unittest.IsolatedAsyncioTestCase):
    def test_document_without_paragraphs_keeps_full_azure_content(self):
        document = SimpleNamespace(
            content="Contract table: amount 100", paragraphs=[],
            tables=[], pages=[], figures=[],
        )
        client = MagicMock()
        client.begin_analyze_document.return_value.result.return_value = document
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "contract.pdf"
            path.write_bytes(b"test pdf")
            with patch.object(DocumentExtractor, "_client", client):
                extraction = DocumentExtractor.extract(str(path))
        self.assertEqual(extraction.text, document.content)
        self.assertEqual(extraction.file_extension, ".pdf")
        self.assertEqual(client.begin_analyze_document.call_args.kwargs["model_id"], "prebuilt-layout")

    async def test_contract_storage_uses_azure_text_without_markdown(self):
        extraction = SimpleNamespace(text="Nội dung hợp đồng Azure")
        item = SimpleNamespace()
        db = AsyncMock()
        with (
            patch("app.services.contract.contract_service.ContractRepository.get_raw_by_hash", new=AsyncMock(return_value=item)) as lookup,
            patch("app.services.contract.contract_service.ContractRepository.update_raw", new=AsyncMock()) as update,
        ):
            result = await ContractService._save_raw(
                db=db, contract_name="Contract", source_file="contract.pdf",
                extraction=extraction,
            )
        self.assertIs(result, item)
        self.assertEqual(item.extracted_content, extraction.text)
        lookup.assert_awaited_once_with(
            db=db, file_hash=hashlib.sha256(extraction.text.encode("utf-8")).hexdigest(),
        )
        update.assert_awaited_once_with(db=db, item=item)
