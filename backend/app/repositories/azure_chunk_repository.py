from azure.core.credentials import (
    AzureKeyCredential
)

from azure.search.documents import (
    SearchClient
)

from app.core.settings import settings





class AzureChunkRepository:

    @staticmethod
    def load_chunks(parent_id: str):

        client = SearchClient(
            endpoint=settings.AZURE_SEARCH_ENDPOINT,

            index_name=
            settings.AZURE_SEARCH_INDEX,

            credential=
            AzureKeyCredential(
                settings.AZURE_SEARCH_KEY
            )
        )

        results = client.search(
            search_text="*",
            filter=
            f"parent_id eq '{parent_id}'",
            top=1000
        )

        return [
            {
                "id":
                    doc["chunk_id"],

                "content":
                    doc["chunk"],
                    
                "sensitivity":
                    doc["sensitivity"],

                "processed":
                    False,

                "tags":
                    [],

                "roles":
                    [],

                "metadata" : {

    "department":
    doc.get("department"),

    "owner_role":
    doc.get("owner_role"),

    "source_file":
    doc.get("source_file"),

    "security_level":
    doc.get("security_level"),

    "document_type":
    doc.get("document_type"),

    "parent_id":
    doc.get("parent_id")
}

            }

            for doc in results
        ]
        
    @staticmethod
    def update_sensitivity(

        chunk_id: str,

        sensitivity: int

    ):


        client = SearchClient(

            endpoint=
            settings
            .AZURE_SEARCH_ENDPOINT,


            index_name=
            settings
            .AZURE_SEARCH_INDEX,


            credential=

            AzureKeyCredential(

                settings
                .AZURE_SEARCH_KEY

            )

        )


        result = (

            client
            .merge_documents([

                {

                    "chunk_id":

                    chunk_id,


                    "sensitivity":

                    sensitivity

                }

            ])

        )
    #     print(
    #     result
    # )
