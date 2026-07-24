from pathlib import Path
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.not_found_exception import (
    NotFoundException,
)

from app.repositories.ai_model_repository import (
    AIModelRepository,
)

from app.repositories.ai_prompt_repository import (
    AIPromptRepository,
)

from app.repositories.recruitment_campaign_repository import (
    RecruitmentCampaignRepository,
)

from app.repositories.recruitment_candidate_repository import (
    RecruitmentCandidateRepository,
)

from app.repositories.recruitment_candidate_result_repository import (
    RecruitmentCandidateResultRepository,
)

from app.services.llm.azure_openai_service import (
    AzureOpenAIService,
)

from app.services.prompt.prompt_builder_azure import (
    PromptBuilderAzure,
)

from app.utils.extract.document_extraction import (
    DocumentExtractor,
)

from app.utils.storage.supabase_storage import (
    SupabaseStorage,
)
from app.enums.prompt_code import PromptCode


class AnalyzeCandidateService:

    @staticmethod
    async def execute(
        db: AsyncSession,
        candidate_id: UUID,
        model_id: UUID,
    ):
        candidate = await RecruitmentCandidateRepository.get_by_id(
            db=db,
            id=candidate_id,
        )

        if candidate is None:
            raise NotFoundException(
                "Candidate not found."
            )

        campaign = await RecruitmentCampaignRepository.get_by_id(
            db=db,
            
            id=candidate.campaign_id,
        )

        if campaign is None:
            raise NotFoundException(
                "Campaign not found."
            )

        prompt = await AIPromptRepository.get_by_code(
            db=db,
            code=PromptCode.RECRUITMENT_DEFAULT,
        )
        if prompt is None:
            raise NotFoundException(
                "Prompt not found."
            )

        model = await AIModelRepository.get_by_id(
            db=db,
            id=model_id,
        )

        if model is None:
            raise NotFoundException(
                "Model not found."
            )

        existed = await RecruitmentCandidateResultRepository.get_by_candidate(
            db=db,
            candidate_id=candidate.id,
        )

        if existed is not None:
            return existed

        local_file = await SupabaseStorage.download_to_temp_file(
            candidate.file_path,
        )

        try:

            extraction = DocumentExtractor.extract(
                local_file,
            )
            print("EXTRACTION:", repr(extraction.text))
            
            print("CV:")
            print(repr(extraction.text[:500]))

            print("JD:")
            print(repr(campaign.job_description[:500]))

            system_prompt, user_prompt = PromptBuilderAzure.build(
                system_prompt=prompt.system_prompt,
                variables={
                    "job_description": campaign.job_description,
                    "cv_text": extraction.text,
                },
            )
            print("SYSTEM PROMPT:", repr(system_prompt))
            print("USER PROMPT:", repr(user_prompt))

            ai = AzureOpenAIService()

            result = await ai.chat(
                model=model.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
            )

            return await RecruitmentCandidateResultRepository.create(
                db=db,
                candidate_id=candidate.id,
                model=model.model_name,
                score=result["score"],
                summary=result.get("summary"),
                strengths=result.get("strengths"),
                weaknesses=result.get("weaknesses"),
                assessment=result.get("assessment"),
                reason=result.get("reason"),
                raw_response=result,
            )

        finally:

            Path(
                local_file
            ).unlink(
                missing_ok=True,
            )