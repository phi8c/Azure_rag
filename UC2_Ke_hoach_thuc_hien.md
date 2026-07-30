# UC2 - Kế hoạch triển khai MVP

## Feature 1. Recruitment Assistant

### 1. Quản lý Job Description

- Xây dựng màn hình quản lý Job Description.
- Upload Job Description.
- Lưu trữ Job Description.
- Hiển thị danh sách Job Description.
- Xem chi tiết Job Description.

---

### 2. Quản lý Candidate

- Upload một hoặc nhiều CV.
- Lưu thông tin Candidate.
- Liên kết Candidate với Job Description.
- Hiển thị danh sách Candidate.

---

### 3. Trích xuất nội dung CV

- Download CV.
- Trích xuất nội dung bằng Docling.
- Chuẩn hóa dữ liệu.
- Lưu kết quả trích xuất.

---

### 4. Đánh giá CV bằng AI

- Đọc Job Description.
- Đọc nội dung CV.
- Xây dựng Prompt.
- Gọi Azure OpenAI.
- Chấm điểm Candidate.
- Đánh giá mức độ phù hợp.
- Sinh Summary.
- Sinh Strengths.
- Sinh Weaknesses.
- Giải thích lý do đánh giá.
- Lưu kết quả đánh giá.

---

### 5. Recruitment Dashboard

- Hiển thị danh sách Candidate.
- Hiển thị điểm đánh giá.
- Hiển thị mức độ phù hợp.
- Hiển thị Summary.
- Hiển thị Strengths / Weaknesses.
- Sắp xếp Candidate theo điểm.

---

### 6. Candidate Chat

- Chat với từng Candidate.
- Trả lời dựa trên:
  - Job Description.
  - CV.
  - AI Review.
- Lưu lịch sử hội thoại.

---

# Feature 2. Project Tracking Assistant

### 1. Microsoft Planner Integration

- Kết nối Microsoft Graph.
- Đọc danh sách Project (Plan).
- Đọc Buckets.
- Đọc Tasks.
- Đọc Assignments.
- Đọc Members.
- Đọc Checklist.
- Đọc Labels.
- Đọc Priority.
- Đọc Progress.
- Đọc Description.
- Đọc Due Date.
- Đọc Attachments.

---

### 2. Đồng bộ dữ liệu Project

- Đồng bộ Project.
- Đồng bộ Member.
- Đồng bộ Task.
- Đồng bộ Assignment.
- Đồng bộ Checklist.
- Đồng bộ Labels.
- Đồng bộ Progress.
- Đồng bộ Timeline.

---

### 3. Xây dựng AI Context

Chuẩn bị dữ liệu cho AI gồm:

- Project Context.
- Team Context.
- Task Context.
- Workload Context.
- Timeline Context.
- Project Policy.

---

### 4. AI Project Analysis

Phân tích:

- Tình trạng Project.
- Tiến độ thực tế.
- Task quá hạn.
- Task ưu tiên.
- Thành viên quá tải.
- Thành viên chưa có task.
- Nguy cơ trễ tiến độ.
- Danh sách rủi ro.
- Đề xuất xử lý.

Lưu kết quả phân tích.

---

### 5. Project Dashboard

Hiển thị:

- Project Summary.
- Overall Progress.
- Task Statistics.
- Risk List.
- Priority Tasks.
- AI Recommendation.
- AI Insight.

---

### 6. Project Chat

Cho phép hỏi đáp về Project.

Ví dụ:

- Tiến độ hiện tại như thế nào?
- Vì sao Project bị chậm?
- Task nào cần ưu tiên?
- Thành viên nào đang quá tải?
- Sprint hiện tại có rủi ro không?

---

### 7. Microsoft Teams Notification

- Phát hiện rủi ro.
- Sinh nội dung cảnh báo.
- Gửi thông báo đến Microsoft Teams.
- Gửi khuyến nghị cho Project Manager.

---

# Feature 3. Cost Dashboard

### 1. Thu thập dữ liệu sử dụng

Lưu:

- Model.
- Prompt.
- Completion.
- Token Input.
- Token Output.
- Cost.
- Latency.
- User.
- Business Module.
- Request Time.

---

### 2. Thống kê chi phí

Tính toán:

- Tổng chi phí.
- Chi phí theo ngày.
- Chi phí theo tháng.
- Chi phí theo Model.
- Chi phí theo User.
- Chi phí theo Business Module.

---

### 3. Cost Dashboard

Hiển thị:

- Tổng Token.
- Tổng Cost.
- Cost theo Model.
- Cost theo User.
- Cost theo Business Module.
- Top Model sử dụng nhiều nhất.
- Top User sử dụng nhiều nhất.
- Biểu đồ chi phí theo thời gian.

---

# Công việc chung

### Prompt Management

- Quản lý Prompt.
- Quản lý Prompt Version.
- Quản lý Prompt theo Business Module.

---



# Thứ tự triển khai

1. Recruitment Assistant.
2. Microsoft Planner Integration.
3. AI Project Analysis.
4. Project Dashboard.
5. Project Chat.
6. Microsoft Teams Notification.
7. Cost Dashboard.
8. Prompt Management.
9. AI Model Management.
10. Audit Log.


** Sau khi thực hiện sẽ tới lập kế hoạch thực hiện tiếp UC1