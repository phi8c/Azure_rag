from botbuilder.core import (

    ActivityHandler,

    TurnContext

)

from app.services.rag.rag_service import (
    RagService
)
from app.enums.prompt_code import PromptCode


class TeamsBotService(

    ActivityHandler

):


    async def on_message_activity(

        self,

        turn_context:
        TurnContext

    ):


        question = (

            turn_context
            .activity
            .text
        )


        rag = (

            RagService()

        )


        channel_data = turn_context.activity.channel_data or {}
        model_id = channel_data.get("model_id")
        if not model_id:
            await turn_context.send_activity("Please supply channelData.model_id.")
            return

        answer = await (

            rag.ask(

                question=

                question,


                chunks=[],
                db=None,
                model_id=model_id,
                mode=PromptCode.INTERNAL,
                workspace_code=PromptCode.CHAT_RAG.value,

            )

        )


        await (

            turn_context

            .send_activity(

                answer
            )

        )
