# Crawl KNIC rồi ingestion qua SharePoint

## Bước 1: tải file thông tin

Backend đang chạy: gọi `POST /documents/crawl/knic` với JSON:

```json
{"max_pages": 30, "max_depth": 2}
```

Ví dụ PowerShell (đổi URL theo backend thực tế):

```powershell
Invoke-WebRequest -Method Post -Uri 'http://localhost:8000/documents/crawl/knic' -ContentType 'application/json' -Body '{"max_pages":30,"max_depth":2}' -OutFile 'knic_company_info.txt'
```

Response là file TXT UTF-8 đính kèm, gồm nội dung từng trang, URL nguồn,
thời điểm crawl và các trang lỗi. Có thể bỏ body để dùng mặc định.
Giới hạn: 1–60 lượt tải trang, độ sâu 0–4, 180 giây cho một request,
3 MB HTML/trang; chỉ theo link HTTPS thuộc `knic.com.vn/vi/`.
Crawl tuần tự, nghỉ 250 ms giữa các lượt. Giới hạn lượt tải tính cả trang lỗi.
Các link chờ còn lại được ghi trong file để nhận biết kết quả chưa đầy đủ.
Nếu một số trang lỗi, file vẫn chứa các trang thành công và danh sách lỗi.
Nếu không có nội dung: HTTP 502. Quá thời gian: HTTP 504; giảm max_pages rồi thử lại.
Không lấy PDF, ảnh, video, trang ngôn ngữ khác hoặc nội dung cần JavaScript.
Đây là nội dung trích xuất, không dùng LLM để suy diễn hay xác minh thông tin.

Hoặc chạy script tại thư mục `backend` với Python đã cài dependencies:

```powershell
python scripts/crawl_knic.py --max-pages 30 --max-depth 2 --output data/knic_company_info.txt
```

## Bước 2: upload và kích hoạt flow

Upload file TXT lên đúng site/drive mà flow ingestion hiện tại theo dõi.
Sau khi upload hoàn tất, gọi API sẵn có:

```powershell
Invoke-RestMethod -Method Post -Uri 'http://localhost:8000/documents/sync'
```

API sync hiện tại gọi Logic App từ `settings.LOGIC_APP_URL` với body `{}`;
site/drive và loại file được xử lý phụ thuộc cấu hình flow đó.
Kiểm tra flow có hỗ trợ TXT trước khi ingestion. `logic_status` trong response
là HTTP status của Logic App; không phải xác nhận ingestion đã hoàn tất.
API crawl chỉ tạo file trả về, chưa upload SharePoint hoặc tự gọi sync.

Kiểm thử riêng (tại `backend`):

```powershell
python -m unittest discover -s tests/api -p test_knic_crawler.py -v
```
