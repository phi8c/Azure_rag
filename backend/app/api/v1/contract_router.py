from uuid import UUID

import shutil
import tempfile

from fastapi import (
    Form,
    UploadFile,
    File,
    Depends,
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