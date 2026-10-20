# Cleanup trước khi build

Đã bỏ:

- Service session memory, conversation summary, query rewrite, message và conversation.
- Local queue trong utils/shared, review worker cũ, queue consumer startup và message/enum chỉ phục vụ worker đó. ReviewService hiện xử lý trực tiếp, không dùng queue.
- API `/conversations/*`, `/graph/*`, `/think/*`.
- Toàn bộ service knowledge/GraphRAG, repository graph/entity và script backfill graph.
- Bước build graph, phân loại chunk và cập nhật sensitivity sau ingestion.
- API `/chunks/unprocessed`, `/chunks/process`, `/chunks/push-sensitivity`.
- `mock_chunks.json`, `review_chunks.json`, dữ liệu cũ trong `temp/` và script thử Cohere/Gemini trong repositories.

Giữ nguyên model DB, repository conversation/message/summary/user-memory.
Không có migration hay thao tác xóa bảng/dữ liệu.
Microsoft Graph phục vụ SharePoint, đăng nhập và meeting vẫn giữ.
ChatConfigCache vẫn cần để cache cấu hình model/prompt; không phải session memory.

Chat web `/chat/query`, `/chat/helpdesk` vẫn stream không lưu lịch sử.
`conversation_id` trong chat web vẫn là mã tương quan do client quản lý.
Teams `/bot/messages` không lưu conversation/message, không rewrite câu hỏi;
cần `model_id` ở body hoặc `channelData.model_id`, dùng mode INTERNAL và
workspace CHAT_RAG. Retrieval dùng object ID và group ID để lọc ACL.

Kiểm tra tại thư mục backend với Python/dependencies hoạt động:

```powershell
python -m compileall -q app
python -m unittest discover -s tests/api -p test_chat_router.py -v
python -m unittest discover -s tests/api -p test_bot_router.py -v
python -m unittest discover -s tests/api -p test_chunk_router.py -v
python -m unittest discover -s tests/api -p test_azure_document_migration.py -v
```

Đây là bước dọn chức năng, chưa tạo hay xác minh bản build Nuitka.
Requirements đã rút từ snapshot toàn venv xuống 20 dependency trực tiếp có pin.
`requirements.txt` vẫn include `requirements.lock.txt` để tương thích CI hiện tại.
Dù tên là `.lock.txt`, danh sách hiện tại chỉ pin dependency trực tiếp;
pip resolve dependency bắc cầu, chưa phải lock đầy đủ được resolver xác minh.
Không cộng số dòng đã xóa thành số package hoặc dung lượng tiết kiệm: nhiều
package vẫn được cài gián tiếp. Cần chạy `pip check` trong môi trường build sạch.

Trích xuất tài liệu chỉ dùng `app/utils/extract/document_intelligent.py` (Azure).
Hợp đồng/CV đã chuyển từ Docling sang Azure Document Intelligence; lưu/hash
nội dung hợp đồng dùng `extraction.text`. Các lần phân tích lại có thể tạo hash
khác so với bản Markdown cũ; dữ liệu DB cũ không bị sửa hay xóa.
Nội dung trả về ưu tiên `AnalyzeResult.content`, fallback sang paragraphs,
để tài liệu chỉ có bảng vẫn có text. CV upload nhận PDF/DOCX, từ chối DOC cũ.

Đã bỏ Docling, Gemini, Groq và factory/failover cũ không còn caller.
Các adapter OpenAI public, Ollama, OpenRouter cũ cũng đã gỡ; LLM chỉ còn
AzureOpenAIService. SDK `openai` vẫn cần cho Azure OpenAI/embedding.
Google Calendar vẫn dùng HTTP OAuth như cũ, không liên quan Google Generative AI.
Đã bỏ các collect-all Docling trong workflow build; không còn dependency trực
tiếp nào trong requirements kéo Torch/Torchvision/Transformers qua Docling.
Build trong venv sạch để không gom lại package từ môi trường cũ. Không uninstall
hay chỉnh sửa các venv hiện có trong đợt này.

`GET /chunks/?parent_id=...` vẫn đọc Azure Search.
`POST /documents/sync` vẫn kích hoạt Logic App như cũ;
`POST /documents/sync-completed` chỉ đặt trạng thái COMPLETED và trả accepted,
không tạo task xử lý chunk hoặc đọc/ghi JSON cục bộ.

`temp/` được ignore và không cần đưa vào artifact. Review upload vẫn tạo mới
`temp/review/<job_id>` khi chạy, nên thư mục làm việc cần có quyền ghi.
Các temp file đang được job cũ tham chiếu sẽ không còn sau cleanup; chỉ job mới
có file upload mới. Với Nuitka/PyInstaller, không thêm temp hoặc hai JSON vào
include-data; `.gitignore` chỉ ngăn thêm vào Git, không phải cấu hình packager.
Workflow hiện tại vẫn dùng PyInstaller, chưa chuyển sang Nuitka.

Kiểm tra trên máy hiện tại bị chặn vì venv trỏ tới Python 3.10 đã không còn.
Rà import tĩnh phát hiện lỗi có sẵn trong `app/models/sync_jobs.py`:
`app.core.database.models.base` không tồn tại. File model này chưa được sửa
trong đợt cleanup; cần xử lý trước khi import hoặc build toàn bộ package.
