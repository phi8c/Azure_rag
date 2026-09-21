import io
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.api.v1.contract_router import (
    analyze_contract_advanced,
)
from app.services.contract.contract_advanced_service import (
    ContractAdvancedService,
)


class ContractAdvancedRouterTest(unittest.IsolatedAsyncioTestCase):

    async def test_temporary_file_is_removed(self):
        observed_path = None

        async def analyze(
            service,
            db,
            file_path,
            model_id,
        ):
            nonlocal observed_path
            observed_path = Path(file_path)
            self.assertTrue(observed_path.is_file())
            self.assertEqual(
                observed_path.read_bytes(),
                b"contract",
            )
            return {
                "company_rule_review": {"results": []},
                "legal_review": {"results": []},
            }

        upload = UploadFile(
            filename="contract.pdf",
            file=io.BytesIO(b"contract"),
        )

        with patch.object(
            ContractAdvancedService,
            "analyze",
            new=analyze,
        ):
            result = await analyze_contract_advanced(
                file=upload,
                model_id=uuid4(),
                db=None,
            )

        self.assertEqual(result["legal_review"], {"results": []})
        self.assertIsNotNone(observed_path)
        self.assertFalse(observed_path.exists())

    async def test_unsupported_file_type_is_rejected(self):
        upload = UploadFile(
            filename="contract.txt",
            file=io.BytesIO(b"contract"),
        )

        with self.assertRaises(HTTPException) as error:
            await analyze_contract_advanced(
                file=upload,
                model_id=uuid4(),
                db=None,
            )

        self.assertEqual(error.exception.status_code, 400)
