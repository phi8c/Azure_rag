from azure.search.documents import (
    SearchClient
)

from azure.core.credentials import (
    AzureKeyCredential
)


from app.core.settings import settings

class AzureSearchService:


    @staticmethod
    def retrieve(

        question:str,

        permissions:list

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


        # print(
        #     azure_filter
        # )


        results = client.search(

            search_text=

            question,


            filter=

            azure_filter,


            top=
            5

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