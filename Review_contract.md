**1. Company Rule Analysis**

- **API:** `POST /contracts/analyze-advanced/company-rule`
- **Content-Type:** `multipart/form-data`
- **Input:**
  - `file`: File PDF hoặc DOCX. (1 file)
  - `model_id`: UUID.
- **Response:** JSON.
- **Dữ liệu trả về:**
  - `company_rule_review`: Kết quả rà soát theo quy định công ty.
  - `contract_content`: String, nội dung hợp đồng đã được extract.

  contract_content yêu cầu phía web app lưu lại vào db để sử dụng cho Legal Contract Analysis và  Legal Chat, vì nó sẽ là đầu vào cho 2 cái API này



**2. Legal Contract Analysis**
  

  API nên được gắn vào 1 nút nó sẽ phân tích dựa trên Luật

- **API:** `POST /contracts/analyze-advanced/legal`
- **Content-Type:** `application/json`
- **Response Content-Type:** `text/event-stream` (SSE).
- **Input:**
  - `model_id`: UUID.
  - `output_extract`: String, nội dung hợp đồng đã extract.
- **Các SSE event trả về:**
  - `started`: Tổng số nội dung cần rà soát.
  - `result`: Kết quả rà soát của từng nội dung.
  - `error`: Thông tin lỗi của một nội dung cụ thể.
  - `completed`: Xác nhận đã xử lý xong.
- Mỗi `result` gồm `contract_text`, `status`, `explanation`, `recommendation` và `sources`.

**3. Legal Chat**

- **API:** `POST /contracts/legal-chat`
- **Content-Type:** `application/json`
- **Input:**
  - `model_id`: UUID.
  - `question`: String, câu hỏi của người dùng.
  - `extracted_contract`: String, nội dung hợp đồng đã extract.
- **Response:** JSON.
- **Dữ liệu trả về:**
  - `answer`: Nội dung trả lời.
  - `retrieval_seeds`: Metadata được dùng để tìm kiếm dữ liệu pháp luật.
  - `sources`: Danh sách nguồn pháp luật tham khảo.