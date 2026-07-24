from app.core.settings import settings
from urllib.parse import urlencode
import httpx
import jwt
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from uuid import UUID

from app.schemas.microsoft_profile import MicrosoftProfile


class MicrosoftAuthService:

    AUTHORITY = (
        f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}"
    )

    AUTHORIZE_ENDPOINT = (
        f"{AUTHORITY}/oauth2/v2.0/authorize"
    )

    TOKEN_ENDPOINT = (
        f"{AUTHORITY}/oauth2/v2.0/token"
    )
    @staticmethod
    def get_login_url() -> str:

        query = {
            "client_id": settings.AZURE_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": settings.MICROSOFT_REDIRECT_URI,
            "response_mode": "query",
            "scope": (
                "openid "
                "profile "
                "email "
                "offline_access "
                "User.Read "
                "Tasks.Read "
                "Group.Read.All"
            ),
        }

        return (
            f"{MicrosoftAuthService.AUTHORIZE_ENDPOINT}"
            f"?{urlencode(query)}"
        )
        
    @staticmethod
    async def exchange_code(
        code: str,
    ):
        payload = {
            "client_id": settings.AZURE_CLIENT_ID,
            "client_secret": settings.AZURE_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.MICROSOFT_REDIRECT_URI,
        }

        async with httpx.AsyncClient() as client:

            response = await client.post(
                MicrosoftAuthService.TOKEN_ENDPOINT,
                data=payload,
            )

            response.raise_for_status()

            token = response.json()

            claims = jwt.decode(
                token["id_token"],
                options={
                    "verify_signature": False,
                },
            )

            token["claims"] = claims

            return token
    

    @staticmethod
    async def get_me(access_token: str):

        async with httpx.AsyncClient() as client:

            response = await client.get(
                "https://graph.microsoft.com/v1.0/me",
                headers={
                    "Authorization": f"Bearer {access_token}"
                }
            )

            response.raise_for_status()

            return response.json()
        
    @staticmethod
    async def authenticate(
        code: str,
    ) -> MicrosoftProfile:

        token = await MicrosoftAuthService.exchange_code(
            code,
        )

        user = await MicrosoftAuthService.get_me(
            token["access_token"],
        )

        claims = token["claims"]

        return MicrosoftProfile(
            tenant_id=UUID(
                claims["tid"],
            ),
            object_id=UUID(
                claims["oid"],
            ),
            email=(
                user["mail"]
                or user["userPrincipalName"]
            ),
            user_principal_name=user[
                "userPrincipalName"
            ],
            display_name=user[
                "displayName"
            ],
            refresh_token=token[
                "refresh_token"
            ],
            access_token=token["access_token"],
            access_token_expires_at=(
                datetime.now(
                    timezone.utc,
                )
                + timedelta(
                    seconds=token[
                        "expires_in"
                    ],
                )
            ),
        )
        
    @staticmethod
    async def refresh_access_token(
        refresh_token: str,
    ) -> dict:

        payload = {
            "client_id": settings.AZURE_CLIENT_ID,
            "client_secret": settings.AZURE_CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "redirect_uri": settings.MICROSOFT_REDIRECT_URI,
        }

        async with httpx.AsyncClient() as client:

            response = await client.post(
                MicrosoftAuthService.TOKEN_ENDPOINT,
                data=payload,
            )

            response.raise_for_status()

            return response.json()