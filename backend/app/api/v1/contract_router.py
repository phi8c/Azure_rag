from uuid import UUID
from pathlib import Path

import shutil
import tempfile

from fastapi import (
    Form,
    UploadFile,
    File,
    Depends,
    HTTPException,
)
from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import (
    get_db
)
from app.services.contract.contract_service import (
    ContractService,
)
from app.services.contract.contract_advanced_service import (
    ContractAdvancedService,
)
from app.schemas.contract_chat_request import ( ContractChatRequest)

router = APIRouter(

    prefix="/contracts",

    tags=["Contracts"],

)



@router.post("/analyze")

async def analyze_contract(

    file: UploadFile = File(...),

    model_id: UUID = Form(...),

    db: AsyncSession = Depends(
        get_db,
    ),

):

    suffix = (
        ".pdf"
        if file.filename.lower().endswith(".pdf")
        else ".docx"
    )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    ) as tmp:

        shutil.copyfileobj(
            file.file,
            tmp,
        )

        file_path = tmp.name

    return await (

        ContractService()

        .analyze(

            db=db,

            file_path=file_path,

            model_id=model_id,

        )

    )
    
    

@router.post("/analyze-advanced")
async def analyze_contract_advanced(
    file: UploadFile = File(...),
    model_id: UUID = Form(...),
    db: AsyncSession = Depends(get_db),
):

    suffix = Path(
        file.filename or ""
    ).suffix.lower()

    if suffix not in {".pdf", ".docx"}:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    file_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as tmp:
            file_path = tmp.name
            shutil.copyfileobj(
                file.file,
                tmp,
            )

        return await (
            ContractAdvancedService()
            .analyze(
                db=db,
                file_path=file_path,
                model_id=model_id,
            )
        )
    finally:
        if file_path:
            Path(file_path).unlink(
                missing_ok=True
            )


@router.post(
    "/chat",
)
async def contract_chat(

    request: ContractChatRequest,

    db: AsyncSession = Depends(
        get_db,
    ),

):

    return await (

        ContractService
        .chat(

            db=db,

            question=request.question,

            model_id=request.model_id,
            
            contract_id=request.contract_id,

        )

    )
    
    
@router.get("")
async def get_contracts(

    db: AsyncSession = Depends(
        get_db,
    ),

):

    return await (

        ContractService
        .get_contracts(

            db=db,

        )

    )
    
@router.get("/{contract_id}")
async def get_contract(

    contract_id: UUID,

    db: AsyncSession = Depends(
        get_db,
    ),

):

    return await (

        ContractService
        .get_contract(

            db=db,

            contract_id=contract_id,

        )

    )
