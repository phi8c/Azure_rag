from azure.search.documents import (
    SearchClient
)

from azure.search.documents.models import (
    VectorizedQuery
)

from azure.core.credentials import (
    AzureKeyCredential
)

from openai import OpenAI

from app.core.settings import settings


class AzureSearchService:

    @staticmethod
    def retrieve(

        question: str,

        permissions: list

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
        print("in ra question trong retrieval", question)

        filters = []

        for p in permissions:

            filters.append(

                "("

                f"department eq "

                f"'{p['department']}' "

                "and "

                f"sensitivity le "

                f"{p['max_sensitivity']}"

                ")"

            )

        azure_filter = (

            " or "

            .join(
                filters
            )

        )

        #
        # EMBEDDING QUERY
        #

        openai_client = OpenAI(

            api_key=
            settings.OPENAI_API_KEY

        )

        embedding_response = (

            openai_client
            .embeddings
            .create(

                model=
                "text-embedding-3-small",

                input=
                question

            )

        )

        query_embedding = (

            embedding_response
            .data[0]
            .embedding

        )

        #
        # VECTOR QUERY
        #

        vector_query = (

            VectorizedQuery(

                vector=
                query_embedding,

                k_nearest_neighbors=
                20,

                fields=
                "text_vector"

            )

        )

        #
        # HYBRID SEARCH
        #

        results = client.search(

            search_text=
            question,

            vector_queries=[
                vector_query
            ],

            filter=
            azure_filter,

            top=
            20

        )

        return [

            {

                "chunk_id":

                doc.get(
                    "chunk_id"
                ),

                "content":

                doc.get(
                    "chunk"
                ),

                "department":

                doc.get(
                    "department"
                ),

                "sensitivity":

                doc.get(
                    "sensitivity"
                )

            }

            for doc

            in results

        ]