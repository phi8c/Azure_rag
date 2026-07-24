from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MicrosoftProfile(BaseModel):

    tenant_id: UUID

    object_id: UUID

    email: str

    user_principal_name: str

    display_name: str

    refresh_token: str
    access_token: str

    access_token_expires_at: datetime