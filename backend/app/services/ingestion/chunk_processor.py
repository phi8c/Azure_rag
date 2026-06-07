from sqlalchemy.ext.asyncio import (
    AsyncSession
)

import json

from app.services.ingestion.sensitivity_classifier import (
    SensitivityClassifier
)


class ChunkProcessor:


    @staticmethod
    async def process_chunk(

        db: AsyncSession,

        chunk: dict

    ):


      

        sensitivity = await (

           SensitivityClassifier
            .detect(

                db=db,


                content=

                chunk["content"],


                security_level=

                chunk[
                    "metadata"
                ].get(
                    "security_level"
                ),


                department=

                chunk[
                    "metadata"
                ].get(
                    "department"
                )

            )
                    )


        # --------------------------
        # Metadata Enrichment
        # --------------------------

        result = {

            "id":

            chunk.get(
                "id"
            ),


            "department":

            
                chunk.get(

                    "metadata",

                    {}

                ).get(

                    "department"

                ),



        "security_level":

        chunk.get(

            "metadata",

            {}

        ).get(

            "security_level"

        ),


            "sensitivity":

            sensitivity,


            "processed":

            True,


            "content_preview":

            chunk.get(
                "content",
                ""
            )[:300]

        }


        # --------------------------
        # Review File
        # --------------------------

        with open(

            "review_chunks.json",

            "a",

            encoding=
            "utf-8"

        ) as f:


            json.dump(

                result,

                f,

                ensure_ascii=False

            )


            f.write(
                "\n"
            )


        return result