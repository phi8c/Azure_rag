import httpx

from app.core.settings import (
    settings
)


class SharePointService:

    LIST_ID = (
        "62207fd2-91ee-4784-9d3a-688adf632a4a"
    )

    @staticmethod
    async def _get_access_token():

        async with httpx.AsyncClient() as client:

            token_response = await client.post(
                f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}/oauth2/v2.0/token",
                data={
                    "client_id":
                    settings.AZURE_CLIENT_ID,

                    "client_secret":
                    settings.AZURE_CLIENT_SECRET,

                    "scope":
                    "https://graph.microsoft.com/.default",

                    "grant_type":
                    "client_credentials"
                }
            )

            token_data = (
                token_response.json()
            )

            print(
                "token_status =",
                token_response.status_code
            )

            print(
                token_data
            )

            return (
                token_data.get(
                    "access_token"
                )
            )
            
    @staticmethod
    async def get_list_item_id(
        drive_item_id: str
    ):

        access_token = await (
            SharePointService
            ._get_access_token()
        )

        async with httpx.AsyncClient() as client:

            url = (

                f"https://graph.microsoft.com/v1.0"

                f"/sites/{settings.SHAREPOINT_SITE_ID}"

                f"/drives/{settings.SHAREPOINT_DRIVE_ID}"

                f"/items/{drive_item_id}"

                f"/listItem"

            )

            response = await client.get(

                url,

                headers={
                    "Authorization":
                    f"Bearer {access_token}"
                }

            )

            print(
                "list_item_status =",
                response.status_code
            )

            print(
                "list_item_body =",
                response.text
            )

            data = response.json()

            return data.get("id")

    @staticmethod
    async def upload_file(
        department: str,
        file_name: str,
        file_content: bytes
    ):

        access_token = await (
            SharePointService
            ._get_access_token()
        )

        async with httpx.AsyncClient() as client:

            upload_url = (
                f"https://graph.microsoft.com/v1.0"
                f"/sites/{settings.SHAREPOINT_SITE_ID}"
                f"/drives/{settings.SHAREPOINT_DRIVE_ID}"
                f"/root:/{department}/{file_name}:/content"
            )

            print(
                "upload_url =",
                upload_url
            )

            response = await client.put(
                upload_url,
                headers={
                    "Authorization":
                    f"Bearer {access_token}",

                    "Content-Type":
                    "application/octet-stream"
                },
                content=file_content
            )

            print(
                "upload_status =",
                response.status_code
            )

            print(
                "upload_body =",
                response.text
            )

            return (
                response.json()
            )

    @staticmethod
    async def update_metadata(

        item_id: str,

        department: str,

        owner_role: str,

        security_level: str,

        document_type: str

    ):

        access_token = await (
            SharePointService
            ._get_access_token()
        )

        async with httpx.AsyncClient() as client:

            metadata_url = (

                f"https://graph.microsoft.com/v1.0"

                f"/sites/{settings.SHAREPOINT_SITE_ID}"

                f"/lists/{SharePointService.LIST_ID}"

                f"/items/{item_id}"

                f"/fields"

            )

            payload = {

                "Ph_x00f2_ngban":
                department,

                "Vaitr_x00f2_s_x1edf_h_x1eef_ut_x1ead_ptin":
                owner_role,

                "L_x1edb_pb_x1ea3_om_x1ead_t":
                security_level,

                "Lo_x1ea1_it_x00e0_ili_x1ec7_u":
                document_type

            }

            print(
                "metadata_url =",
                metadata_url
            )

            print(
                "payload =",
                payload
            )

            response = await client.patch(

                metadata_url,

                headers={

                    "Authorization":
                    f"Bearer {access_token}",

                    "Content-Type":
                    "application/json"

                },

                json=payload

            )

            print(
                "metadata_status =",
                response.status_code
            )

            print(
                "metadata_body =",
                response.text
            )

            return (
                response.json()
            )