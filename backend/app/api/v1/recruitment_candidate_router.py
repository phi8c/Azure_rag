from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)

from uuid import UUID

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import (
    get_db
)

from app.schemas.recruitment_schema import (
    RecruitmentCampaignCreate,
    RecruitmentCampaignResponse
)

from app.services.recruitment.recruitment_service import (
    RecruitmentService
)

from app.services.recruitment.upload_candidate import (
    UploadCandidateService,
)
from app.services.recruitment.analyze_candidate_service import (
    AnalyzeCandidateService,
)
from app.schemas.analyze_candidate_request import (
    AnalyzeCandidateRequest,
)

router = APIRouter(
    prefix="/recruitments",
    tags=["Recruitments"]
)


@router.post(
    "",
    response_model=RecruitmentCampaignResponse
)
async def create_campaign(
    payload: RecruitmentCampaignCreate,
    db: AsyncSession = Depends(get_db)
):
    return await (
        RecruitmentService.create_campaign(
            db=db,
            role_id=payload.role_id,
            title=payload.title,
            job_description=payload.job_description
        )
    )
    
@router.post(
    "/{campaign_id}/candidates",
)
async def upload_candidate(
    campaign_id: UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    return await UploadCandidateService.execute(
        db=db,
        campaign_id=campaign_id,
        file=file,
    )
    
@router.post(
    "/candidates/{candidate_id}/analyze",
)
async def analyze_candidate(
    candidate_id: UUID,
    request: AnalyzeCandidateRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await AnalyzeCandidateService.execute(
        db=db,
        candidate_id=candidate_id,
        model_id=request.model_id,
    )

    return result