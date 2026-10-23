import json
import re

from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from fastapi.responses import StreamingResponse

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.database import (
    get_db
)

from app.schemas.chat_schema import (
    ChatRequest,
)

from app.repositories.conversation_repository import ConversationRepository

from app.services.azure.azure_search_service import (
    AzureSearchService
)

from app.services.rag.rag_service import (
    RagService
)

from app.enums.prompt_code import (
    PromptCode
)

from app.services.rag.chat_config_cache import (
    ChatConfigCache
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


#
# top_k mặc định khi workspace chưa có rag config
#

CHAT_RAG_DEFAULT_TOP_K = 10

HELPDESK_DEFAULT_TOP_K = 20


SMALLTALK_EXACT = {
    "chào", "xin chào", "chao", "hi", "hello", "hey", "alo",
    "ok", "oke", "okie", "cảm ơn", "cám ơn", "thanks", "thank you",
    "tạm biệt", "bye", "bạn khỏe không", "bạn khoẻ không",
    "bạn có khỏe không", "bạn là ai", "bạn tên gì",
}

SMALLTALK_START = ("chào", "xin chào", "cảm ơn", "cám ơn", "bạn khỏe", "bạn khoẻ")


def is_smalltalk(question: str) -> bool:
    """Câu xã giao ngắn (chào, hỏi thăm, cảm ơn): không cần tìm tài liệu."""
    text = " ".join(re.sub(r"[^\w\s]", " ", question.lower()).split())

    if not text:
        return True

    if text in SMALLTALK_EXACT:
        return True

    return len(text.split()) <= 6 and text.startswith(SMALLTALK_START)


def sse_event(
    event: str,
    data,
) -> str:

    return (
        f"event: {event}\n"
        f"data: {json.dumps(data, ensure_ascii=False, default=str)}\n\n"
    )


def build_internal_sources(
    chunks: list,
) -> list:

    source_map = {}

    for chunk in chunks:

        file = chunk["source_file"]

        if file not in source_map:

            source_map[file] = {
                "source_file": file,
                "source_url": chunk["source_url"],
                "drive_id": chunk.get("drive_id"),
                "drive_item_id": chunk.get("drive_item_id"),
                "excerpt": chunk["content"],
                "type": "internal",
            }

    return list(source_map.values())


class PublicAnswerStreamParser:

    def __init__(self):

        self._buffer = ""
        self._position = 0
        self._started = False
        self._finished = False
        self._escaped = False
        self._unicode_escape = ""

    def feed(
        self,
        token: str,
    ) -> str:

        self._buffer += token
        delta = []

        while self._position < len(self._buffer):

            char = self._buffer[self._position]

            if not self._started:

                key_position = self._buffer.find(
                    '"answer"',
                    self._position,
                )

                if key_position < 0:
                    self._position = max(
                        0,
                        len(self._buffer) - len('"answer"'),
                    )
                    break

                colon_position = self._buffer.find(
                    ":",
                    key_position + len('"answer"'),
                )

                if colon_position < 0:
                    self._position = key_position
                    break

                quote_position = self._buffer.find(
                    '"',
                    colon_position + 1,
                )

                if quote_position < 0:
                    self._position = key_position
                    break

                self._position = quote_position + 1
                self._started = True
                continue

            if self._finished:
                break

            if self._unicode_escape:

                needed = 4 - len(self._unicode_escape)
                self._unicode_escape += self._buffer[
                    self._position:self._position + needed
                ]
                self._position += min(
                    needed,
                    len(self._buffer) - self._position,
                )

                if len(self._unicode_escape) < 4:
                    break

                delta.append(
                    chr(
                        int(
                            self._unicode_escape,
                            16,
                        )
                    )
                )
                self._unicode_escape = ""
                self._escaped = False
                continue

            if self._escaped:

                escape_map = {
                    '"': '"',
                    "\\": "\\",
                    "/": "/",
                    "b": "\b",
                    "f": "\f",
                    "n": "\n",
                    "r": "\r",
                    "t": "\t",
                }

                if char == "u":
                    self._unicode_escape = ""
                else:
                    delta.append(
                        escape_map.get(
                            char,
                            char,
                        )
                    )
                    self._escaped = False

                self._position += 1
                continue

            if char == "\\":
                self._escaped = True
                self._position += 1
                continue

            if char == '"':
                self._finished = True
                self._position += 1
                break

            delta.append(char)
            self._position += 1

        return "".join(delta)


def parse_public_answer(
    raw_answer: str,
    streamed_answer: str,
) -> tuple[str, list]:

    try:

        result = json.loads(raw_answer)

        return (
            result["answer"],
            result["sources"],
        )

    except json.JSONDecodeError:

        return (
            streamed_answer or raw_answer,
            [],
        )


async def stream_chat(
    body: ChatRequest,
    db: AsyncSession,
    workspace_code: str,
    default_top_k: int,
    retrieve,
    track_conversation: bool = False,
) -> StreamingResponse:

    #
    # The client manages the conversation ID; the public query endpoint keeps
    # only its request counter in the conversations table.
    #

    conversation_uuid = body.conversation_id or uuid4()
    conversation_id = str(conversation_uuid)

    is_public = body.mode == PromptCode.PUBLIC

    rag_service = RagService()

    #
    # Kiểm tra trước khi stream: cấu hình đọc từ cache trong RAM
    # (không chạm DB), nên lỗi vẫn trả 400/404 mà gần như không tốn thời gian.
    #

    try:

        chat_config = await rag_service.load_chat_config(
            db=db,
            model_id=body.model_id,
            mode=body.mode,
            workspace_code=workspace_code,
        )


    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except LookupError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    # The landing-page widget supplies a stable UUID. Store one counter per
    # conversation; a returned zero means this is every third request.
    should_suggest_contact = False
    if track_conversation and body.mode == PromptCode.INTERNAL:
        request_count = await ConversationRepository.increment_chat_request_count(
            db=db,
            conversation_id=conversation_uuid,
        )
        should_suggest_contact = request_count == 0

    if should_suggest_contact:
        chat_config = dict(chat_config)
        chat_config["system_prompt"] += (
            "\n\nHãy kết thúc câu trả lời này bằng lời mời tự nhiên: "
            "‘Quý khách có thể để lại họ tên, email và số điện thoại trong cuộc trò chuyện "
            "này để bên chúng tôi liên hệ hỗ trợ.’ Nếu câu trả lời cần theo định dạng JSON, "
            "đặt lời mời trong trường answer và giữ nguyên định dạng JSON bắt buộc."
        )

    top_k = (
        await ChatConfigCache.get_top_k(workspace_code)
        or default_top_k
    )

    async def stream_response():

        raw_answer = ""
        full_answer = ""
        chunks = []
        final_sources = None if is_public else []
        public_parser = (
            PublicAnswerStreamParser()
            if is_public
            else None
        )

        #
        # Retrieval chạy bên trong stream để header HTTP được trả ngay
        #

        if not is_public and not is_smalltalk(body.question):

            try:

                chunks = await retrieve(
                    question=body.question,
                    top_k=top_k,
                )

            except Exception as exc:

                print(
                    "chat retrieval error =",
                    repr(exc),
                )

                yield sse_event(
                    "error",
                    {
                        "conversation_id": conversation_id,
                        "message": "Failed to retrieve documents.",
                    },
                )

                return

            final_sources = build_internal_sources(chunks)

        effective_config = chat_config

        #
        # INTERNAL chỉ trả lời từ tài liệu; không có context thì dùng COMBINE
        # để model vẫn trò chuyện bình thường (không nhắc "không có dữ liệu")
        #

        if not is_public and not chunks and body.mode == PromptCode.INTERNAL:

            try:

                effective_config = await rag_service.load_chat_config(
                    db=db,
                    model_id=body.model_id,
                    mode=PromptCode.COMBINE,
                    workspace_code=workspace_code,
                )

            except LookupError:

                effective_config = chat_config

        yield sse_event(
            "metadata",
            {
                "conversation_id": conversation_id,
                "title": body.question,
                "sources": final_sources,
            },
        )

        try:

            async for token in rag_service.ask_stream(
                chat_config=effective_config,
                question=body.question,
                chunks=chunks,
            ):

                raw_answer += token

                answer_delta = token

                if public_parser is not None:

                    answer_delta = public_parser.feed(token)

                if answer_delta:

                    full_answer += answer_delta

                    yield sse_event(
                        "answer",
                        {
                            "delta": answer_delta,
                        },
                    )

        except Exception as exc:

            print(
                "chat stream error =",
                repr(exc),
            )

            yield sse_event(
                "error",
                {
                    "conversation_id": conversation_id,
                    "message": "Failed to generate answer.",
                },
            )

            return

        if is_public:

            full_answer, final_sources = parse_public_answer(
                raw_answer=raw_answer,
                streamed_answer=full_answer,
            )

            yield sse_event(
                "metadata",
                {
                    "conversation_id": conversation_id,
                    "title": body.question,
                    "sources": final_sources,
                },
            )

        yield sse_event(
            "done",
            {
                "conversation_id": conversation_id,
                "title": body.question,
                "answer": full_answer,
                "sources": final_sources,
            },
        )

    return StreamingResponse(
        stream_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/query")
async def query(
    body: ChatRequest,
    db: AsyncSession = Depends(
        get_db,
    ),
):

    return await stream_chat(
        body=body,
        db=db,
        workspace_code=PromptCode.CHAT_RAG.value,
        default_top_k=CHAT_RAG_DEFAULT_TOP_K,
        retrieve=AzureSearchService.retrieve,
        track_conversation=True,
    )


@router.post("/helpdesk")
async def helpdesk_query(
    body: ChatRequest,
    db: AsyncSession = Depends(
        get_db,
    ),
):

    return await stream_chat(
        body=body,
        db=db,
        workspace_code=PromptCode.HELPDESK.value,
        default_top_k=HELPDESK_DEFAULT_TOP_K,
        retrieve=AzureSearchService.retrieve_helpdesk,
    )
