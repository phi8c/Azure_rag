**Tích hợp SSO và Chat API**

Web App thực hiện đăng nhập Microsoft 365/Entra ID và cần lấy được:

- `microsoft_object_id`: Object ID của user trong Entra ID.
- `group_ids`: Danh sách ID các Entra group mà user tham gia.

Không cần gửi group name, role nội bộ hoặc Microsoft access token cho Chat API.

**1. Chat Query**

- Method: `POST`
- Endpoint: `/chat/query`
- Content-Type: `application/json`
- Response: `text/event-stream` (SSE)

**2. Helpdesk Chat**

- Method: `POST`
- Endpoint: `/chat/helpdesk`
- Content-Type: `application/json`
- Response: `text/event-stream` (SSE)

Hai API sử dụng chung request:

```json
{
  "conversation_id": null,
  "question": "Nội dung câu hỏi",
  "model_id": "MODEL_ID",
  "mode": "CHAT_RAG",
  "microsoft_object_id": "ENTRA_USER_OBJECT_ID",
  "group_ids": [
    "ENTRA_GROUP_ID_1",
    "ENTRA_GROUP_ID_2"
  ]
}
```

`conversation_id` có thể để `null` khi bắt đầu hội thoại. Client sử dụng ID được trả về trong SSE cho các câu hỏi tiếp theo. `mode` phải là giá trị hợp lệ trong `PromptCode`.

**Response SSE**

Các event chính:

- `metadata`: thông tin conversation và nguồn tài liệu.
- `answer`: từng phần nội dung câu trả lời.
- `done`: kết quả hoàn chỉnh.

**Phân quyền tài liệu**

Khi đồng bộ tài liệu từ SharePoint vào Azure AI Search, mỗi document cần có:

- `allowed_user_ids`: các Entra user Object ID được phép đọc.
- `allowed_group_ids`: các Entra group ID được phép đọc.

User được phép retrieval khi Object ID của họ nằm trong `allowed_user_ids`, hoặc có ít nhất một group thuộc `allowed_group_ids`.

Phase hiện tại chưa sử dụng `allowed_sharepoint_group_ids`. Web App phải lấy identity từ phiên SSO thực tế; không cho người dùng tự nhập hoặc chỉnh sửa các giá trị permission này.


Bạn gửi FE đoạn này là đủ:

> API `/api/contracts/analyze-advanced/legal` trả kết quả theo **SSE**, hiện backend đã trả đầy đủ nội dung review. FE đang có vẻ đọc nhầm object bên ngoài nên chỉ hiển thị `index` và `total`.
>
> Mỗi `event: result` có dạng:
>
> ```json
> {
>   "index": 0,
>   "total": 5,
>   "result": {
>     "contract_text": "...",
>     "status": "RISK",
>     "explanation": "...",
>     "recommendation": "...",
>     "sources": [
>       {
>         "document_id": "39917",
>         "title": "...",
>         "doc_type": "Nghị định",
>         "doc_number": null
>       }
>     ]
>   }
> }
> ```
>
> `index` và `total` chỉ dùng để theo dõi progress. Nội dung cần hiển thị nằm trong `data.result`. :chatgpt-content-reference{index="0"}
>
> FE cần render:
>
> ```text
> result.contract_text
> result.status
> result.explanation
> result.recommendation
> result.sources
> ```
>
> `sources` là array, có thể có nhiều nguồn nên hiển thị danh sách nguồn theo từng review. Hiện source có `document_id`, `title`, `doc_type`, `doc_number`. Ví dụ một review hiện tại có tới 3 nguồn. :chatgpt-content-reference{index="1"}
>
> Flow SSE là:
>
> ```text
> started → result → result → ... → completed
> ```
>
> `started/completed` và `index/total` chỉ phục vụ trạng thái/progress, không phải nội dung review.