import json
import unittest
from unittest.mock import AsyncMock, patch

from app.enums.prompt_code import PromptCode
from app.services.contract.contract_advanced_service import (
    ContractAdvancedService,
)
from app.services.llm.azure_openai_service import (
    LLMResponseTruncatedError,
)


class ContractAdvancedServiceTest(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.service = ContractAdvancedService.__new__(
            ContractAdvancedService
        )
        self.service.llm = AsyncMock()

    def test_validate_analyzer_result_with_both_pipelines(self):
        result = self.service._validate_analyzer_result(
            {
                "company_rule_checks": [
                    {
                        "contract_text": "Company clause",
                        "retrieval_seeds": [" approval ", None],
                    }
                ],
                "legal_checks": [
                    {
                        "contract_text": "Legal clause",
                        "metadata_seeds": {
                            "legal_area": [" contracts ", None],
                        },
                    }
                ],
            }
        )

        self.assertEqual(
            result["company_rule_checks"][0]["retrieval_seeds"],
            ["approval"],
        )
        self.assertEqual(
            result["legal_checks"][0]["metadata_seeds"],
            {"legal_area": ["contracts"]},
        )

    def test_validate_analyzer_result_enforces_latency_limits(self):
        result = self.service._validate_analyzer_result(
            {
                "company_rule_checks": [
                    {
                        "contract_text": f"Company clause {index}",
                        "retrieval_seeds": ["first", "second"],
                    }
                    for index in range(10)
                ],
                "legal_checks": [
                    {
                        "contract_text": f"Legal clause {index}",
                        "metadata_seeds": {
                            "title": ["first", "second"],
                            "legal_area": ["first", "second"],
                        },
                    }
                    for index in range(10)
                ],
            }
        )

        self.assertEqual(len(result["company_rule_checks"]), 8)
        self.assertEqual(len(result["legal_checks"]), 8)
        self.assertEqual(
            result["company_rule_checks"][0]["retrieval_seeds"],
            ["first"],
        )
        self.assertEqual(
            result["legal_checks"][0]["metadata_seeds"],
            {"title": ["first"], "legal_area": ["first"]},
        )

    async def test_analyze_runs_both_retrieval_pipelines(self):
        model = type(
            "Model",
            (),
            {"model_name": "deployment"},
        )()
        model_config = type(
            "ModelConfig",
            (),
            {"temperature": 0.2, "max_tokens": 2000},
        )()
        analysis = {
            "company_rule_checks": [
                {
                    "contract_text": "Company clause",
                    "retrieval_seeds": ["approval"],
                }
            ],
            "legal_checks": [
                {
                    "contract_text": "Legal clause",
                    "metadata_seeds": {
                        "title": ["contracts"],
                    },
                }
            ],
        }
        company_data = [
            {"contract_text": "Company clause", "contexts": []}
        ]
        legal_data = [
            {"contract_text": "Legal clause", "contexts": []}
        ]

        with (
            patch(
                "app.services.contract.contract_advanced_service."
                "AIModelRepository.get_by_id",
                new=AsyncMock(return_value=model),
            ),
            patch(
                "app.services.contract.contract_advanced_service."
                "WorkspaceConfigRepository."
                "get_model_config_by_workspace_code",
                new=AsyncMock(return_value=model_config),
            ),
            patch.object(
                self.service,
                "_extract_contract",
                return_value="Contract body",
            ),
            patch.object(
                self.service,
                "_analyze_contract_for_retrieval",
                new=AsyncMock(return_value=analysis),
            ),
            patch.object(
                self.service,
                "_load_prompt",
                new=AsyncMock(return_value=object()),
            ),
            patch(
                "app.services.contract.contract_advanced_service."
                "CompanyPolicyRetrievalService.retrieve",
                new=AsyncMock(return_value=company_data),
            ) as company_retrieve,
            patch(
                "app.services.contract.contract_advanced_service."
                "LegalRetrievalService.retrieve",
                return_value=legal_data,
            ) as legal_retrieve,
            patch.object(
                self.service,
                "_review_company_rules",
                new=AsyncMock(return_value={"results": []}),
            ) as company_review,
            patch.object(
                self.service,
                "_review_legal",
                new=AsyncMock(return_value={"results": []}),
            ) as legal_review,
        ):
            result = await self.service.analyze(
                db=None,
                file_path="contract.pdf",
                model_id=None,
            )

        company_retrieve.assert_awaited_once_with(
            analysis["company_rule_checks"]
        )
        legal_retrieve.assert_called_once_with(
            analysis["legal_checks"]
        )
        company_review.assert_awaited_once()
        legal_review.assert_awaited_once()
        self.assertEqual(
            result,
            {
                "company_rule_review": {"results": []},
                "legal_review": {"results": []},
            },
        )

    async def test_empty_company_checks_skip_reviewer(self):
        result = await self.service._review_company_rules(
            db=None,
            review_data=[],
            model_name="unused",
            temperature=0.0,
            max_tokens=100,
        )

        self.assertEqual(result, {"results": []})
        self.service.llm.chat_json.assert_not_awaited()

    async def test_empty_legal_checks_skip_reviewer(self):
        result = await self.service._review_legal(
            db=None,
            review_data=[],
            model_name="unused",
            temperature=0.0,
            max_tokens=100,
        )

        self.assertEqual(result, {"results": []})
        self.service.llm.chat_json.assert_not_awaited()

    def test_malformed_llm_json_raises(self):
        with self.assertRaises(json.JSONDecodeError):
            self.service._parse_json_object("not json")

    async def test_call_llm_uses_system_and_user_prompts(self):
        prompt = type(
            "Prompt",
            (),
            {
                "system_prompt": "System prompt",
                "user_prompt": "Review {{contract_content}}",
            },
        )()
        self.service.llm.chat_json.return_value = "{}"

        with patch(
            "app.services.contract.contract_advanced_service."
            "AIPromptRepository.get_by_code",
            new=AsyncMock(return_value=prompt),
        ):
            await self.service._call_llm_json(
                db=None,
                prompt_code=PromptCode.CONTRACT_REVIEW_ANALYZER,
                placeholder="{{contract_content}}",
                placeholder_value="Contract body",
                model_name="deployment",
                temperature=0.2,
                max_tokens=2000,
            )

        messages = self.service.llm.chat_json.await_args.kwargs[
            "messages"
        ]
        self.assertEqual(messages[0]["content"], "System prompt")
        self.assertEqual(
            messages[1]["content"],
            "Review Contract body",
        )

    async def test_truncated_json_raises_without_retry(self):
        prompt = type(
            "Prompt",
            (),
            {
                "system_prompt": "System prompt",
                "user_prompt": "Review {{contract_content}}",
            },
        )()
        self.service.llm.chat_json.side_effect = (
            LLMResponseTruncatedError("truncated")
        )

        with patch(
            "app.services.contract.contract_advanced_service."
            "AIPromptRepository.get_by_code",
            new=AsyncMock(return_value=prompt),
        ):
            with self.assertRaises(LLMResponseTruncatedError):
                await self.service._call_llm_json(
                    db=None,
                    prompt_code=PromptCode.CONTRACT_REVIEW_ANALYZER,
                    placeholder="{{contract_content}}",
                    placeholder_value="Contract body",
                    model_name="deployment",
                    temperature=0.2,
                    max_tokens=2000,
                )

        self.service.llm.chat_json.assert_awaited_once()
        self.assertEqual(
            self.service.llm.chat_json.await_args.kwargs[
                "max_completion_tokens"
            ],
            2000,
        )
