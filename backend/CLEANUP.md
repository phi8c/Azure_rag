# Cleanup trước khi build

Đã bỏ:

- Service session memory, conversation summary, query rewrite, message và conversation.
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
```

Đây là bước dọn chức năng, chưa tạo hay xác minh bản build Nuitka.
Requirements đã rút từ snapshot toàn venv xuống 25 dependency trực tiếp có pin.
`requirements.txt` vẫn include `requirements.lock.txt` để tương thích CI hiện tại.
Dù tên là `.lock.txt`, danh sách hiện tại chỉ pin dependency trực tiếp;
pip resolve dependency bắc cầu, chưa phải lock đầy đủ được resolver xác minh.
Không cộng số dòng đã xóa thành số package hoặc dung lượng tiết kiệm: nhiều
package vẫn được cài gián tiếp. Cần chạy `pip check` trong môi trường build sạch.

Không có import trực tiếp Torch/Torchvision/Transformers trong app. Tuy nhiên,
`contract_service.py` và `analyze_candidate_service.py` dùng DocumentExtractor
ở `app/utils/extract/document_extraction.py`, chạy Docling.
Metadata cục bộ: docling -> docling-slim[standard] -> torch, torchvision,
docling-ibm-models -> transformers. Do đó vẫn giữ Docling, để pip cài các dependency
này và không exclude chúng khỏi artifact khi chưa thay bộ trích xuất.

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
