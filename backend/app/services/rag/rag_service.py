from app.services.llm.ollama_service import (
    OllamaService
)
from app.services.session_memory.session_memory_service import (
    SessionMemoryService
)


class RagService:


    def __init__(

        self

    ):

        self.llm = (

            OllamaService()
    
        )


    async def ask(

        self,
        
        db,
        
        conversation_id: str,

        question:
        str,

        chunks:
        list

    ):
        
        memory_context = await (
            SessionMemoryService
            .build_context(
                db=db,
                conversation_id=conversation_id
            )
        )
        
        recent_messages = memory_context


        context = (

            "\n\n"

            .join(

                chunk["content"]

                for chunk

                in chunks

                if chunk.get(
                    "content"
                )

            )

        )


        prompt = f"""

Bạn là trợ lý nội bộ doanh nghiệp.

Bạn là trợ lý nội bộ doanh nghiệp. Hãy trả lời câu hỏi dựa trên bộ ngữ cảnh (Context) được cung cấp. Dựa theo bối cảnh trước đó mà người dùng đã hỏi (recent_message)




Yêu cầu nghiêm ngặt:
1. Trả lời chi tiết, tổng hợp TOÀN BỘ các ý liên quan từ Context. Tuyệt đối không lược bỏ bất kỳ chi tiết nào.
2. Trình bày rõ ràng, mạch lạc (bắt buộc dùng gạch đầu dòng nếu câu trả lời gồm nhiều thông tin/nhiều ý khác nhau).
3. Chỉ dùng thông tin có trong Context. Nếu Context không có thông tin để trả lời, chỉ cần đáp: "Không tìm thấy thông tin phù hợp."

RECENT CONVERSATION
------------------

{recent_messages}



Context:

{context}



Question:

{question}

"""


        answer = await (

            self.llm
            .generate(

                prompt
            )

        )


        return answer