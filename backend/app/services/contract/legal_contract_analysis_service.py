import asyncio
import json
from collections import Counter
from time import perf_counter
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contract_advanced_logging import contract_split_logger
from app.enums.prompt_code import PromptCode
from app.repositories.ai_model_repository import AIModelRepository
from app.repositories.ai_prompt_repository import AIPromptRepository
from app.repositories.rag_config_repository import (
    WorkspaceConfigRepository,
)
from app.services.contract.legal_chat_retrieval_service import (
    LegalChatRetrievalService,
)
from app.services.llm.azure_openai_service import AzureOpenAIService


class LegalContractAnalysisService:
    MAX_LEGAL_CHECKS = 8
    MAX_SEEDS_PER_METADATA_FIELD = 2
    RETRIEVAL_CONCURRENCY = 4
    ALLOWED_METADATA_FIELDS = {
            "doc_type",
            "doc_number",
            "year",
            "issuer",
            "issuer_kind",
            "tier",
            "tier_name",
            "legal_area",
            "section",
            "title",
            "source",
            "issue_date",
            "effective_date",
            "status",
            "update_date",
            "signer",
            "issuing_body",
            "parent_acts",
            "article_titles",
            "citations",
    }

    def __init__(self):
        self.llm = AzureOpenAIService()

    async def analyze(
        self,
        db: AsyncSession,
        model_id: UUID,
        output_extract: str,
    ) -> dict[str, Any]:
        total_started_at = perf_counter()
        model, model_config = await self._load_model_context(
            db=db,
            model_id=model_id,
        )

        started_at = perf_counter()
        analyzer_prompt = await self._load_prompt(
            db=db,
            prompt_code=PromptCode.LEGAL_CONTRACT_ANALYZER,
        )
        analyzer_result = await self._call_analyzer(
            prompt=analyzer_prompt,
            output_extract=output_extract,
            model_name=model.model_name,
            temperature=float(model_config.temperature),
            max_tokens=int(model_config.max_tokens),
        )
        legal_checks = self._validate_analyzer_result(analyzer_result)
        contract_split_logger.info(
            "[LEGAL_CONTRACT][TIMING] analyzer=%.3fs checks=%d",
            perf_counter() - started_at,
            len(legal_checks),
        )

        if not legal_checks:
            contract_split_logger.info(
                "[LEGAL_CONTRACT][TIMING] retrieval=0.000s"
            )
            contract_split_logger.info(
                "[LEGAL_CONTRACT][TIMING] reviewer=0.000s"
            )
            contract_split_logger.info(
                "[LEGAL_CONTRACT][TIMING] total=%.3fs",
                perf_counter() - total_started_at,
            )
            return {"results": []}

        started_at = perf_counter()
        review_data = await self._retrieve_legal_context(legal_checks)
        contract_split_logger.info(
            "[LEGAL_CONTRACT][TIMING] retrieval=%.3fs documents=%d",
            perf_counter() - started_at,
            sum(len(item["legal_context"]) for item in review_data),
        )

        started_at = perf_counter()
        reviewer_prompt = await self._load_prompt(
            db=db,
            prompt_code=PromptCode.LEGAL_CONTRACT_REVIEWER,
        )
        reviewer_result = await self._call_reviewer(
            prompt=reviewer_prompt,
            review_data=review_data,
            model_name=model.model_name,
            temperature=float(model_config.temperature),
            max_tokens=int(model_config.max_tokens),
        )
        response = self._validate_reviewer_result(
            reviewer_result,
            legal_checks,
        )
        contract_split_logger.info(
            "[LEGAL_CONTRACT][TIMING] reviewer=%.3fs",
            perf_counter() - started_at,
        )
        contract_split_logger.info(
            "[LEGAL_CONTRACT][TIMING] total=%.3fs",
            perf_counter() - total_started_at,
        )

        return response

    async def _retrieve_legal_context(
        self,
        legal_checks: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        semaphore = asyncio.Semaphore(self.RETRIEVAL_CONCURRENCY)

        async def retrieve_one(index: int, check: dict[str, Any]):
            async with semaphore:
                documents = await asyncio.to_thread(
                    LegalChatRetrievalService.retrieve,
                    check["metadata_seeds"],
                )
                return index, {
                    "contract_text": check["contract_text"],
                    "legal_context": documents,
                }

        results = await asyncio.gather(
            *[
                retrieve_one(index, check)
                for index, check in enumerate(legal_checks)
            ]
        )
        results.sort(key=lambda item: item[0])

        return [item[1] for item in results]

    async def _call_analyzer(
        self,
        prompt,
        output_extract: str,
        model_name: str,
        temperature: float,
        max_tokens: int,
    ) -> dict[str, Any]:
        user_prompt = self._render_prompt(
            template=prompt.user_prompt,
            replacements={
                "{{extracted_contract}}": output_extract,
            },
            prompt_code=PromptCode.LEGAL_CONTRACT_ANALYZER,
        )
        response = await self.llm.chat_json(
            model=model_name,
            messages=self._messages(prompt.system_prompt, user_prompt),
            temperature=temperature,
            max_completion_tokens=max_tokens,
        )

        return self._parse_json_object(response)

    async def _call_reviewer(
        self,
        prompt,
        review_data: list[dict[str, Any]],
        model_name: str,
        temperature: float,
        max_tokens: int,
    ) -> dict[str, Any]:
        user_prompt = self._render_prompt(
            template=prompt.user_prompt,
            replacements={
                "{{legal_review_data}}": json.dumps(
                    review_data,
                    ensure_ascii=False,
                ),
            },
            prompt_code=PromptCode.LEGAL_CONTRACT_REVIEWER,
        )
        response = await self.llm.chat_json(
            model=model_name,
            messages=self._messages(prompt.system_prompt, user_prompt),
            temperature=temperature,
            max_completion_tokens=max_tokens,
        )

        return self._parse_json_object(response)

    @classmethod
    def _validate_analyzer_result(
        cls,
        result: Any,
    ) -> list[dict[str, Any]]:
        if not isinstance(result, dict):
            raise ValueError(
                "Legal Contract Analyzer response must be an object."
            )

        checks = result.get("legal_checks")

        if not isinstance(checks, list):
            raise ValueError("legal_checks must be a list.")

        return [
            cls._validate_legal_check(check)
            for check in checks[:cls.MAX_LEGAL_CHECKS]
        ]

    @classmethod
    def _validate_legal_check(cls, check: Any) -> dict[str, Any]:
        if not isinstance(check, dict):
            raise ValueError("Each legal check must be an object.")

        contract_text = check.get("contract_text")
        metadata_seeds = check.get("metadata_seeds")

        if (
            not isinstance(contract_text, str)
            or not contract_text.strip()
        ):
            raise ValueError(
                "Legal check contract_text must be a non-empty string."
            )

        if not isinstance(metadata_seeds, dict):
            raise ValueError(
                "Legal check metadata_seeds must be an object."
            )

        normalized = {}

        for field, values in metadata_seeds.items():
            if field not in cls.ALLOWED_METADATA_FIELDS:
                continue

            if not isinstance(values, list):
                raise ValueError(
                    f"Metadata seeds for {field} must be a list."
                )

            normalized_values = []
            seen = set()

            for value in values:
                if not isinstance(value, str):
                    continue

                value = value.strip()

                if not value or value in seen:
                    continue

                seen.add(value)
                normalized_values.append(value)

                if (
                    len(normalized_values)
                    >= cls.MAX_SEEDS_PER_METADATA_FIELD
                ):
                    break

            if normalized_values:
                normalized[field] = normalized_values

        if not normalized:
            raise ValueError(
                "Legal check must contain at least one valid metadata seed."
            )

        return {
            "contract_text": contract_text,
            "metadata_seeds": normalized,
        }

    @staticmethod
    def _validate_reviewer_result(
        result: Any,
        legal_checks: list[dict[str, Any]],
    ) -> dict[str, Any]:
        if not isinstance(result, dict):
            raise ValueError(
                "Legal Contract Reviewer response must be an object."
            )

        results = result.get("results")

        if not isinstance(results, list):
            raise ValueError("Legal reviewer results must be a list.")

        sanitized_results = []

        for item in results:
            if not isinstance(item, dict):
                raise ValueError(
                    "Each legal reviewer result must be an object."
                )

            contract_text = item.get("contract_text")
            status = item.get("status")
            explanation = item.get("explanation")
            recommendation = item.get("recommendation")
            sources = item.get("sources")

            if not isinstance(contract_text, str):
                raise ValueError(
                    "Reviewer result contract_text must be a string."
                )

            if status not in {"COMPLIANT", "RISK", "UNCLEAR"}:
                raise ValueError("Reviewer result status is invalid.")

            if not isinstance(explanation, str):
                raise ValueError(
                    "Reviewer result explanation must be a string."
                )

            if not isinstance(recommendation, str):
                raise ValueError(
                    "Reviewer result recommendation must be a string."
                )

            if not isinstance(sources, list):
                raise ValueError(
                    "Reviewer result sources must be a list."
                )

            sanitized_results.append(
                {
                    "contract_text": contract_text,
                    "status": status,
                    "explanation": explanation,
                    "recommendation": recommendation,
                    "sources": [
                        {
                            key: value
                            for key, value in source.items()
                            if key != "vn_text"
                        }
                        for source in sources
                        if isinstance(source, dict)
                    ],
                }
            )

        expected = [check["contract_text"] for check in legal_checks]
        actual = [item["contract_text"] for item in sanitized_results]

        if Counter(expected) != Counter(actual):
            raise ValueError(
                "Legal reviewer results do not match legal checks."
            )

        return {"results": sanitized_results}

    @staticmethod
    def _parse_json_object(response: str) -> dict[str, Any]:
        content = response.strip()

        if content.startswith("```"):
            lines = content.splitlines()[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            content = "\n".join(lines).strip()

        result = json.loads(content)

        if not isinstance(result, dict):
            raise ValueError("LLM response must be a JSON object.")

        return result

    @staticmethod
    def _render_prompt(
        template: str,
        replacements: dict[str, str],
        prompt_code: PromptCode,
    ) -> str:
        rendered = template

        for placeholder, value in replacements.items():
            if placeholder not in rendered:
                raise ValueError(
                    f"Prompt {prompt_code.value} is missing "
                    f"placeholder {placeholder}."
                )

            rendered = rendered.replace(placeholder, value)

        return rendered

    @staticmethod
    def _messages(
        system_prompt: str,
        user_prompt: str,
    ) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    @staticmethod
    async def _load_model_context(
        db: AsyncSession,
        model_id: UUID,
    ):
        model = await AIModelRepository.get_by_id(db=db, id=model_id)

        if model is None:
            raise LookupError("AI model not found.")

        model_config = await (
            WorkspaceConfigRepository
            .get_model_config_by_workspace_code(
                db=db,
                workspace_code=PromptCode.CONTRACT_ANALYZE.value,
            )
        )

        if model_config is None:
            raise LookupError(
                "Workspace model config for CONTRACT_ANALYZE not found."
            )

        return model, model_config

    @staticmethod
    async def _load_prompt(
        db: AsyncSession,
        prompt_code: PromptCode,
    ):
        prompt = await AIPromptRepository.get_by_code(
            db=db,
            code=prompt_code,
        )

        if prompt is None:
            raise LookupError(
                f"Prompt {prompt_code.value} not found."
            )

        return prompt
