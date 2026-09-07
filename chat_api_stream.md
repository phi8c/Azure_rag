Dưới đây là format tích hợp cho FE.

Hai API đã chuyển sang stream SSE:

```http
POST /chat/query
POST /chat/helpdesk
Content-Type: application/json
Accept: text/event-stream
```

Request body giữ như cũ:

```json
{
  "conversation_id": null,
  "question": "Nội dung câu hỏi",
  "role_id": 1,
  "model_id": "31d8f3f4-7a46-4be4-8984-6de1249533ec",
  "mode": "PUBLIC"
}
```

Response không còn là JSON thường nữa, mà là `text/event-stream`.

Các event trả về:

```text
event: metadata
data: {"conversation_id":"...","title":"...","sources":null}

event: answer
data: {"delta":"Nội dung "}

event: answer
data: {"delta":"trả lời "}

event: answer
data: {"delta":"được stream..."}

event: done
data: {"conversation_id":"...","title":"...","answer":"Full answer","sources":[...]}
```

Ý nghĩa:

```ts
metadata
```

Trả thông tin ban đầu. Có thể có `sources: null` ở đầu, đặc biệt với `PUBLIC`.

```ts
answer
```

Mỗi event chứa một phần text mới trong `data.delta`. FE append `delta` vào message assistant hiện tại.

```ts
done
```

Event cuối cùng. Chứa full payload hoàn chỉnh:

```json
{
  "conversation_id": "...",
  "title": "...",
  "answer": "Full answer",
  "sources": []
}
```

FE nên dùng `done.answer` để đồng bộ lại nội dung cuối cùng, và dùng `done.sources` để hiển thị nguồn tham khảo.

Ví dụ tích hợp bằng `fetch`:

```ts
async function streamChat({
  endpoint,
  body,
  onMetadata,
  onDelta,
  onDone,
}: {
  endpoint: "/chat/query" | "/chat/helpdesk";
  body: any;
  onMetadata?: (data: any) => void;
  onDelta?: (delta: string) => void;
  onDone?: (data: any) => void;
}) {
  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    },
    body: JSON.stringify(body),
  });

  if (!response.ok || !response.body) {
    throw new Error("Chat stream request failed");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");

  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();

    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    const events = buffer.split("\n\n");
    buffer = events.pop() || "";

    for (const rawEvent of events) {
      const lines = rawEvent.split("\n");

      const eventLine = lines.find((line) => line.startsWith("event:"));
      const dataLine = lines.find((line) => line.startsWith("data:"));

      if (!eventLine || !dataLine) continue;

      const eventName = eventLine.replace("event:", "").trim();
      const data = JSON.parse(dataLine.replace("data:", "").trim());

      if (eventName === "metadata") {
        onMetadata?.(data);
      }

      if (eventName === "answer") {
        onDelta?.(data.delta || "");
      }

      if (eventName === "done") {
        onDone?.(data);
      }
    }
  }
}
```

Ví dụ dùng cho `/chat/query`:

```ts
let assistantText = "";

await streamChat({
  endpoint: "/chat/query",
  body: {
    conversation_id: null,
    question: "Trình bày về quản lý vật tư",
    role_id: 1,
    model_id: "31d8f3f4-7a46-4be4-8984-6de1249533ec",
    mode: "PUBLIC",
  },
  onMetadata: (data) => {
    console.log("metadata", data);
  },
  onDelta: (delta) => {
    assistantText += delta;
    console.log("streaming answer", assistantText);
  },
  onDone: (data) => {
    assistantText = data.answer;
    console.log("final answer", data.answer);
    console.log("sources", data.sources);
  },
});
```

`/chat/helpdesk` dùng y hệt, chỉ đổi endpoint:

```ts
endpoint: "/chat/helpdesk"
```

FE không cần xử lý riêng theo mode. `PUBLIC`, `INTERNAL`, `COMBINE` đều đọc cùng event format: `metadata`, `answer`, `done`.