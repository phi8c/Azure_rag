







Chat RAG
API: POST
 https://ai.sadec.co/api/chat/query

Theo tài liệu, API hãy dùng cho module Helpdesk HR/IT và Hỏi đáp tài liệu
2 module này sẽ tạm thời dùng chung API này



body:
{
  "conversation_id": "1af91f54-0c95-4021-bb18-a42b5aa65871",
  "role_id": 1,
  "question": "trình bày cái bối cảnh tái cấu trúc và định hướng số hóa",
  "model_id": "31d8f3f4-7a46-4be4-8984-6de1249533ec",
  "mode": "INTERNAL"
}

trong đó mode gồm có: INTERNAL, PUBLIC, COMBINE
INTERNAL là chat RAG thuần
PUBLIC là không dùng dữ liệu đã build mà do model hoàn toàn trả lời
COMBINE là kết hợp cả 2, model sẽ có quyền bổ sung những ý thiếu sót

response

{
  "conversation_id": "1af91f54-0c95-4021-bb18-a42b5aa65871",
  "title": "trình bày cái bối cảnh tái cấu trúc và định hướng số hóa",
  "answer": "1.1. Bối cảnh tái cấu trúc và định hướng số hóa\n\nTập đoàn Công nghệ và Bán lẻ AST đang bước vào giai đoạn bản lề..... Định hướng số hóa buộc chúng ta phải dịch chuyển nguồn lực từ các vị trí vận hành thuần túy sang các vị trí phân tích dữ liệu, vận hành hệ thống và quản trị trải nghiệm khách hàng một cách tinh gọn nhất.",
  "sources": [
    {
      "source_file": "HR_Ke_Hoach_Tai_Cau_Truc_Nhan_Su_Du_An_Alpha_2026.docx",
      "excerpt": "1.1. Bối cảnh tái cấu trúc và định hướng số hóa\n\nSự thay đổi này đồng nghĩa với việc các quy trình thủ công truyền thống không còn phù hợp..... Định hướng số hóa buộc chúng ta phải dịch chuyển nguồn lực từ các vị trí vận hành thuần túy sang các vị trí phân tích dữ liệu, vận hành hệ thống và quản trị trải nghiệm khách hàng một cách tinh gọn nhất.",
      "type": "internal"
    },
    {
      "source_file": "HopDongBatDongSan_OCR (2).docx",
      "excerpt": "6.2 Hình ảnh và bản đồ minh họa (Dùng cho kiểm tra OCR)\n\nDưới đây là hình ảnh bản đồ mô phỏng vị trí và thông số cơ bản của thửa đất.....",
      "type": "internal"
    },
    {
      "source_file": "HopDongBatDongSan_OCR (1).docx",
      "excerpt": "6.2 Hình ảnh và bản đồ minh họa (Dùng cho kiểm tra OCR)\n\nDưới đây là hình ảnh bản đồ mô phỏng vị trí và thông số cơ bản của thửa đất.....",
      "type": "internal"
    }
  ]
}















//////////////////////////////////////////////////////////////////////////////////////////////
POST: https://ai.sadec.co/api/recruitments/analyze 
API phân tích CV cho module Tuyển dụng
Note: Đã trả sẵn score để ranking
input: Multipart form 

model_id: 31d8f3f4-7a46-4be4-8984-6de1249533ec
files: nhiều file, tối đa 5 file
job_description: str


response

{
  "job_id": "c4b77a00-c513-4ecc-9df0-878672ef940a",
  "status": "COMPLETED",
  "total_files": 2,
  "results": [
    {
      "task_id": "26f3dd20-5bd0-43c2-8fd7-dd7251ba2f56",
      "file_name": "CV_Middle_Java_NguyenVanA.pdf",
      "status": "COMPLETED",
      "review_result": {
        "score": 92,
        "assessment": "Strong Hire",
        "reason": "Ứng viên có hơn 3 năm kinh nghiệm đúng với vị trí Middle Java Developer (yêu cầu 2–4 năm), tập trung vào backend Java và Spring Boot. Kỹ năng chuyên môn phù hợp chặt chẽ với JD: nắm vững OOP, Design Patterns, làm việc với Spring Boot, Spring MVC, Spring Data JPA/Hibernate, RESTful API, Unit Test (JUnit, Mockito) và tham gia Code Review. Ứng viên có kinh nghiệm rõ ràng với cơ sở dữ liệu quan hệ (MySQL, PostgreSQL, Oracle) và NoSQL (MongoDB), cùng Redis cho caching, đáp ứng tốt yêu cầu tối ưu truy vấn và hiệu năng. Về công nghệ mở rộng, ứng viên đã làm với Microservices, RabbitMQ, Kafka, Docker, Jenkins, Git, Maven/Gradle, rất sát với phần ưu tiên trong JD. Kinh nghiệm làm việc trong môi trường Agile/Scrum, phối hợp với QA/QC, Frontend được mô tả cụ thể. Trình độ học vấn đúng chuyên ngành (ĐH Bách Khoa, Kỹ thuật Phần mềm). Điểm còn thiếu là chưa thấy đề cập Kubernetes, Memcached, cũng như không có chứng chỉ chuyên môn. Tuy nhiên, mức độ khớp với JD rất cao, đặc biệt về backend Java, hiệu năng và kiến trúc Microservices.",
        "summary": "Ứng viên phù hợp rất cao với vị trí Middle Java Developer, cả về kinh nghiệm lẫn công nghệ. Hồ sơ thể hiện rõ năng lực backend Java, Spring Boot, cơ sở dữ liệu và Microservices. Một số công nghệ ưu tiên như Kubernetes, Memcached chưa được đề cập, nhưng không ảnh hưởng lớn đến mức độ phù hợp tổng thể.",
        "strengths": [
          "Kinh nghiệm 3+ năm làm Java Backend, đúng dải Middle (2–4 năm) theo yêu cầu JD",
          "Thành thạo Java 11/17, OOP, Design Patterns, RESTful API, phù hợp với yêu cầu nền tảng Java",
          "Kinh nghiệm sâu với Spring Boot, Spring MVC, Spring Data JPA/Hibernate và Spring Security",
          "Làm việc với nhiều hệ quản trị CSDL quan hệ (MySQL, PostgreSQL, Oracle) và tối ưu truy vấn SQL",
          "Có kinh nghiệm với NoSQL (MongoDB) và Redis cho caching, đáp ứng yêu cầu về NoSQL và bộ nhớ đệm",
          "Trải nghiệm thực tế với kiến trúc Microservices và Message Broker (RabbitMQ, Kafka)",
          "Sử dụng thành thạo Git, Maven, Gradle, Docker, Jenkins, phù hợp yêu cầu về công cụ và DevOps cơ bản",
          "Tham gia viết Unit Test (JUnit, Mockito) và Code Review, chú trọng chất lượng mã nguồn",
          "Đã làm việc trong môi trường Agile/Scrum, phối hợp với QA/QC, Frontend và BA",
          "Tốt nghiệp đại học chuyên ngành Kỹ thuật Phần mềm, đúng yêu cầu học vấn"
        ],
        "weaknesses": [
          "Không thấy đề cập đến Kubernetes, trong khi JD ưu tiên ứng viên có kinh nghiệm Docker/Kubernetes",
          "Không nêu kinh nghiệm với Memcached (chỉ có Redis), trong khi JD nhắc đến Redis/Memcached",
          "Không liệt kê chứng chỉ chuyên môn (Java, Spring, Database, v.v.) nếu công ty ưu tiên ứng viên có chứng chỉ",
          "Chưa mô tả chi tiết về mức độ tham gia thiết kế kiến trúc tổng thể (architecture) ngoài phạm vi module/dự án cụ thể",
          "Không có thông tin về kinh nghiệm bảo mật nâng cao ngoài Spring Security cơ bản (ví dụ: OWASP, hardening hệ thống)"
        ]
      }
    },
    {
      "task_id": "6af7181a-dbe7-4ea3-8750-f66365e77cb7",
      "file_name": "CV_Middle_Backend_Python.pdf",
      "status": "COMPLETED",
      "review_result": {
        "score": 55,
        "assessment": "Consider",
        "reason": "Ứng viên có hơn 2 năm kinh nghiệm backend, nền tảng OOP tốt và đã làm việc với RESTful API, microservices, message queues, Redis, PostgreSQL/MySQL, Git, Docker, CI/CD, AWS. Đây là các yếu tố phù hợp với yêu cầu về kinh nghiệm backend, kiến trúc, hiệu năng và hệ thống phân tán trong JD. Tuy nhiên, toàn bộ kinh nghiệm thực tế đều xoay quanh Python (FastAPI, Django, Flask), không có bất kỳ kinh nghiệm Java hay Spring Boot/Spring MVC/Spring Data JPA nào được nêu trong CV. JD yêu cầu rõ 2–4 năm kinh nghiệm Java Developer và thành thạo hệ sinh thái Java, nên đây là khoảng trống lớn. Ứng viên cũng không đề cập đến unit test trong Java, công cụ build Java (Maven/Gradle), hay kinh nghiệm với Kafka/Kubernetes. Trình độ học vấn đúng chuyên ngành CNTT, có dự án tốt nghiệp và dự án cá nhân thể hiện khả năng thiết kế hệ thống. Tổng thể, ứng viên phù hợp về tư duy backend và hệ thống nhưng thiếu công nghệ cốt lõi Java, nên chỉ phù hợp nếu công ty chấp nhận chuyển đổi công nghệ.",
        "summary": "Ứng viên là backend developer Python với hơn 2 năm kinh nghiệm, nền tảng OOP và hệ thống backend khá tốt. Tuy nhiên, CV không thể hiện bất kỳ kinh nghiệm Java/Spring nào, trong khi JD yêu cầu rõ Middle Java Developer. Có thể cân nhắc nếu công ty mở cho việc chuyển đổi từ Python sang Java, còn nếu yêu cầu Java bắt buộc thì mức độ phù hợp thấp.",
        "strengths": [
          "Hơn 2 năm kinh nghiệm phát triển backend với RESTful API, phù hợp mức seniority Middle về mặt kinh nghiệm tổng thể",
          "Kinh nghiệm tối ưu hiệu năng hệ thống và truy vấn SQL (giảm thời gian phản hồi API, tối ưu query trên PostgreSQL)",
          "Đã làm việc với cơ sở dữ liệu quan hệ (PostgreSQL, MySQL) và NoSQL (MongoDB), cùng Redis làm cache/bộ nhớ đệm",
          "Kinh nghiệm với microservices, message queues (RabbitMQ, Celery) và triển khai trên môi trường cloud (AWS, Docker, CI/CD)",
          "Tham gia Agile/Scrum, code review, viết tài liệu API, thể hiện khả năng làm việc nhóm và quy trình phát triển chuẩn",
          "Tốt nghiệp đại học chuyên ngành CNTT, có dự án tốt nghiệp và dự án cá nhân thể hiện khả năng tự triển khai hệ thống"
        ],
        "weaknesses": [
          "Không có bất kỳ kinh nghiệm hoặc kỹ năng Java được nêu trong CV, trong khi JD yêu cầu Middle Java Developer",
          "Không đề cập đến Spring Boot, Spring MVC, Spring Data JPA hay bất kỳ framework nào trong hệ sinh thái Java",
          "Không thể hiện kinh nghiệm với công cụ build Java như Maven hoặc Gradle",
          "Không nêu kinh nghiệm với unit test trong Java (JUnit, etc.), chỉ có Pytest cho Python",
          "Không đề cập đến Kafka hoặc Kubernetes, trong khi đây là điểm ưu tiên trong JD",
          "Không có thông tin về việc thiết kế kiến trúc hệ thống và cơ sở dữ liệu trong bối cảnh Java, chỉ thể hiện ở môi trường Python"
        ]
      }
    }
  ]
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////
Tracking Project Task Module theo dõi tiến độ dự án


/////
POST: http://localhost:8000/documents/sync/projects
Không cần gửi tham số gì trong body
API này có thể được gắn vào khi nhấn đến Tab Theo dõi tiến độ trên sidebar, API này sẽ load các file xlsx và phân tích các file đó lưu vào db
Hoặc không cần thiết phải gắn vào Tab, mà gắn nó trên một nút coi như một cách để thực hiện thủ công vì logic của API này đã được set chạy worker tự động mỗi 30 phút 1 lần. 

response
[
  {
    "project": {
      "ProjectCode": "AGENT5",
      "ProjectName": "Agent 5 - Data Q&A điều hành",
      "ProjectManager": "Nguyễn Văn A",
      "Customer": "KN Holding",
      "StartDate": "2026-07-01",
      "EndDate": "2026-10-30",
      "Budget": 2000000000,
      "CurrentSpent": 1250000000,
      "Status": "In Progress",
      "LastUpdated": "2026-08-03 10:30"
    },
    "tasks": [
      {
        "TaskId": "T001",
        "Sprint": "Sprint 5",
        "Epic": "Authentication",
        "Module": "Backend",
        "Task": "Implement SSO Login",
        "Owner": "An",
        "Priority": "High",
        "StoryPoint": 8,
        "Status": "Completed",
        "ProgressPercent": 100,
        "StartDate": "2026-07-20",
        "DueDate": "2026-07-28",
        "CompletedDate": "2026-07-27",
        "EstimatedHours": 24,
        "ActualHours": 22,
        "Blocked": "No",
        "RiskLevel": "Low",
        "LastUpdated": "2026-07-27"
      },
      {
        "TaskId": "T002",
        "Sprint": "Sprint 5",
        "Epic": "Authentication",
        "Module": "Frontend",
        "Task": "Login UI",
        "Owner": "Bình",
        "Priority": "Medium",
        "StoryPoint": 5,
        "Status": "In Progress",
        "ProgressPercent": 70,
        "StartDate": "2026-07-24",
        "DueDate": "2026-08-05",
        "EstimatedHours": 16,
        "ActualHours": 12,
        "Blocked": "No",
        "RiskLevel": "Low",
        "LastUpdated": "2026-08-03"
      },
      {
        "TaskId": "T003",
        "Sprint": "Sprint 5",
        "Epic": "RAG",
        "Module": "Backend",
        "Task": "Azure Search Integration",
        "Owner": "Cường",
        "Priority": "High",
        "StoryPoint": 13,
        "Status": "Blocked",
        "ProgressPercent": 45,
        "StartDate": "2026-07-25",
        "DueDate": "2026-08-02",
        "EstimatedHours": 40,
        "ActualHours": 28,
        "Blocked": "Yes",
        "BlockReason": "Waiting Azure permission",
        "RiskLevel": "High",
        "LastUpdated": "2026-08-03"
      },
      {
        "TaskId": "T004",
        "Sprint": "Sprint 5",
        "Epic": "Dashboard",
        "Module": "Frontend",
        "Task": "Project Dashboard",
        "Owner": "Dung",
        "Priority": "High",
        "StoryPoint": 8,
        "Status": "Late",
        "ProgressPercent": 60,
        "StartDate": "2026-07-22",
        "DueDate": "2026-08-01",
        "EstimatedHours": 24,
        "ActualHours": 30,
        "Blocked": "No",
        "RiskLevel": "High",
        "LastUpdated": "2026-08-03"
      },
      {
        "TaskId": "T005",
        "Sprint": "Sprint 6",
        "Epic": "AI Chat",
        "Module": "Backend",
        "Task": "AI Summary API",
        "Owner": "An",
        "Priority": "High",
        "StoryPoint": 8,
        "Status": "Not Started",
        "ProgressPercent": 0,
        "StartDate": "2026-08-04",
        "DueDate": "2026-08-10",
        "EstimatedHours": 24,
        "ActualHours": 0,
        "Blocked": "No",
        "RiskLevel": "Medium",
        "LastUpdated": "2026-08-03"
      },
      {
        "TaskId": "T006",
        "Sprint": "Sprint 6",
        "Epic": "Notification",
        "Module": "Backend",
        "Task": "Teams Notification",
        "Owner": "Hà",
        "Priority": "Low",
        "StoryPoint": 3,
        "Status": "Completed",
        "ProgressPercent": 100,
        "StartDate": "2026-07-21",
        "DueDate": "2026-07-25",
        "CompletedDate": "2026-07-25",
        "EstimatedHours": 8,
        "ActualHours": 7,
        "Blocked": "No",
        "RiskLevel": "Low",
        "LastUpdated": "2026-07-25"
      }
    ],
    "members": [
      {
        "Member": "An",
        "Role": "Backend",
        "CapacityHoursPerWeek": 40,
        "CurrentAllocatedHours": 38,
        "Team": "Platform"
      },
      {
        "Member": "Bình",
        "Role": "Frontend",
        "CapacityHoursPerWeek": 40,
        "CurrentAllocatedHours": 30,
        "Team": "Web"
      },
      {
        "Member": "Cường",
        "Role": "Backend",
        "CapacityHoursPerWeek": 40,
        "CurrentAllocatedHours": 44,
        "Team": "Platform"
      },
      {
        "Member": "Dung",
        "Role": "Frontend",
        "CapacityHoursPerWeek": 40,
        "CurrentAllocatedHours": 42,
        "Team": "Web"
      },
      {
        "Member": "Hà",
        "Role": "Backend",
        "CapacityHoursPerWeek": 40,
        "CurrentAllocatedHours": 16,
        "Team": "Platform"
      }
    ],
    "risks": [
      {
        "RiskId": "R001",
        "Description": "Azure permission delays",
        "Impact": "High",
        "Owner": "Cường",
        "Status": "Open",
        "LastUpdated": "2026-08-03"
      },
      {
        "RiskId": "R002",
        "Description": "Frontend dashboard behind schedule",
        "Impact": "Medium",
        "Owner": "Dung",
        "Status": "Open",
        "LastUpdated": "2026-08-03"
      }
    ],
    "project_code": "AI"
  }
]

///
Lấy danh sách dự án đã có trong db (sau mỗi lần sync sẽ cập nhật vào db) để hiển thị theo mockup giao diện
API sẽ trả về thông tin để hiển thị đầy đủ thông tin như trong mockup trong module theo dõi tiến độ
GET: https://ai.sadec.co/api/documents/project-tracking/projects

response:
[
  {
    "project_code": "AI",
    "project_name": "Agent 5 - Data Q&A điều hành",
    "progress": {
      "status": "WARNING",
      "title": "Có nguy cơ chậm tiến độ"
    },
    "budget": {
      "status": "SUCCESS",
      "title": "Trong ngân sách"
    },
    "risk": {
      "count": 2,
      "total": 6
    }
  }
]

/////// 
Lấy chi tiết 1 dự án bằng project code khi nhấn xem task trên mỗi record list project

API: GET

https://ai.sadec.co/api/documents/project-tracking/projects/{project_code}
ví dụ:

https://ai.sadec.co/api/documents/project-tracking/projects/AI


Note: Trên mỗi record hiển thị chi tiết sẽ có nút nguyên nhân, hãy lấy trường summary trong thông tin trả về để hiển thị




response:


{
  "project_code": "AI",
  "project_name": "Agent 5 - Data Q&A điều hành",
  "dashboard": {
    "summary": "Dự án đang trong ngân sách nhưng có một số hạng mục bị chậm và bị chặn..... Cần ưu tiên xử lý blocker và điều chỉnh kế hoạch cho các task rủi ro.",
    "overall_health": {
      "status": "WARNING",
      "title": "Cần theo dõi"
    },
    "progress": {
      "status": "WARNING",
      "title": "Có nguy cơ chậm tiến độ"
    },
    "budget": {
      "status": "SUCCESS",
      "title": "Trong ngân sách"
    },
    "risk": {
      "count": 2,
      "total": 6
    },
    "task_analysis": [
      {
        "status": "Blocked",
        "task_id": "T003",
        "task_name": "Azure Search Integration",
        "root_cause": "Task bị chặn do đang chờ quyền truy cập Azure (Waiting Azure permission).",
        "recommendation": "Ưu tiên xử lý blocker bằng cách làm việc với bộ phận/khách hàng phụ trách Azure để cấp quyền sớm....."
      },
      {
        "status": "Late",
        "task_id": "T004",
        "task_name": "Project Dashboard",
        "root_cause": "Task đã quá hạn (Status = Late) và ActualHours đã vượt EstimatedHours.....",
        "recommendation": "Điều chỉnh kế hoạch Sprint và xem xét hỗ trợ thêm nhân sự Frontend hoặc giảm phạm vi để hoàn thành Dashboard đúng yêu cầu."
      }
    ]
  },
  "project": {
    "risks": [
      {
        "RiskId": "R001",
        "Owner": "Cường",
        "Impact": "High",
        "Status": "Open",
        "Description": "Azure permission delays",
        "LastUpdated": "2026-08-03"
      },
      {
        "RiskId": "R002",
        "Owner": "Dung",
        "Impact": "Medium",
        "Status": "Open",
        "Description": "Frontend dashboard behind schedule",
        "LastUpdated": "2026-08-03"
      }
    ],
    "tasks": [
      {
        "TaskId": "T001",
        "Epic": "Authentication",
        "Task": "Implement SSO Login",
        "Owner": "An",
        "Module": "Backend",
        "Sprint": "Sprint 5",
        "Status": "Completed",
        "Blocked": "No",
        "DueDate": "2026-07-28",
        "Priority": "High",
        "RiskLevel": "Low",
        "StartDate": "2026-07-20",
        "StoryPoint": 8,
        "ActualHours": 22,
        "EstimatedHours": 24,
        "ProgressPercent": 100,
        "CompletedDate": "2026-07-27",
        "LastUpdated": "2026-07-27"
      },
      {
        "TaskId": "T002",
        "Epic": "Authentication",
        "Task": "Login UI",
        "Owner": "Bình",
        "Module": "Frontend",
        "Sprint": "Sprint 5",
        "Status": "In Progress",
        "Blocked": "No",
        "DueDate": "2026-08-05",
        "Priority": "Medium",
        "RiskLevel": "Low",
        "StartDate": "2026-07-24",
        "StoryPoint": 5,
        "ActualHours": 12,
        "EstimatedHours": 16,
        "ProgressPercent": 70,
        "LastUpdated": "2026-08-03"
      },
      {
        "TaskId": "T003",
        "Epic": "RAG",
        "Task": "Azure Search Integration",
        "Owner": "Cường",
        "Module": "Backend",
        "Sprint": "Sprint 5",
        "Status": "Blocked",
        "Blocked": "Yes",
        "BlockReason": "Waiting Azure permission",
        "DueDate": "2026-08-02",
        "Priority": "High",
        "RiskLevel": "High",
        "StartDate": "2026-07-25",
        "StoryPoint": 13,
        "ActualHours": 28,
        "EstimatedHours": 40,
        "ProgressPercent": 45,
        "LastUpdated": "2026-08-03"
      },
      {
        "TaskId": "T004",
        "Epic": "Dashboard",
        "Task": "Project Dashboard",
        "Owner": "Dung",
        "Module": "Frontend",
        "Sprint": "Sprint 5",
        "Status": "Late",
        "Blocked": "No",
        "DueDate": "2026-08-01",
        "Priority": "High",
        "RiskLevel": "High",
        "StartDate": "2026-07-22",
        "StoryPoint": 8,
        "ActualHours": 30,
        "EstimatedHours": 24,
        "ProgressPercent": 60,
        "LastUpdated": "2026-08-03"
      },
      {
        "TaskId": "T005",
        "Epic": "AI Chat",
        "Task": "AI Summary API",
        "Owner": "An",
        "Module": "Backend",
        "Sprint": "Sprint 6",
        "Status": "Not Started",
        "Blocked": "No",
        "DueDate": "2026-08-10",
        "Priority": "High",
        "RiskLevel": "Medium",
        "StartDate": "2026-08-04",
        "StoryPoint": 8,
        "ActualHours": 0,
        "EstimatedHours": 24,
        "ProgressPercent": 0,
        "LastUpdated": "2026-08-03"
      },
      {
        "TaskId": "T006",
        "Epic": "Notification",
        "Task": "Teams Notification",
        "Owner": "Hà",
        "Module": "Backend",
        "Sprint": "Sprint 6",
        "Status": "Completed",
        "Blocked": "No",
        "DueDate": "2026-07-25",
        "Priority": "Low",
        "RiskLevel": "Low",
        "StartDate": "2026-07-21",
        "StoryPoint": 3,
        "ActualHours": 7,
        "EstimatedHours": 8,
        "ProgressPercent": 100,
        "CompletedDate": "2026-07-25",
        "LastUpdated": "2026-07-25"
      }
    ],
    "members": [
      {
        "Member": "An",
        "Role": "Backend",
        "Team": "Platform",
        "CapacityHoursPerWeek": 40,
        "CurrentAllocatedHours": 38
      },
      {
        "Member": "Bình",
        "Role": "Frontend",
        "Team": "Web",
        "CapacityHoursPerWeek": 40,
        "CurrentAllocatedHours": 30
      },
      {
        "Member": "Cường",
        "Role": "Backend",
        "Team": "Platform",
        "CapacityHoursPerWeek": 40,
        "CurrentAllocatedHours": 44
      },
      {
        "Member": "Dung",
        "Role": "Frontend",
        "Team": "Web",
        "CapacityHoursPerWeek": 40,
        "CurrentAllocatedHours": 42
      },
      {
        "Member": "Hà",
        "Role": "Backend",
        "Team": "Platform",
        "CapacityHoursPerWeek": 40,
        "CurrentAllocatedHours": 16
      }
    ],
    "project_details": {
      "ProjectCode": "AGENT5",
      "ProjectName": "Agent 5 - Data Q&A điều hành",
      "ProjectManager": "Nguyễn Văn A",
      "Customer": "KN Holding",
      "Status": "In Progress",
      "StartDate": "2026-07-01",
      "EndDate": "2026-10-30",
      "Budget": 2000000000,
      "CurrentSpent": 1250000000,
      "LastUpdated": "2026-08-03 10:30"
    }
  }
}






POST: https://ai.sadec.co/api/documents/tracking/chat

body:
{
  "question": "dự án Agent 5 - Data Q&A điều hành tình trạng hiện như nào",
  "model_id": "31d8f3f4-7a46-4be4-8984-6de1249533ec"
}

response:


{
  "answer": "Tình trạng hiện tại của dự án “Agent 5 - Data Q&A điều hành”:\n\n1) Tổng quan dự án\n- Trạng thái: In Progress (đang triển khai)\n- Thời gian: \n  - StartDate: 2026-07-01\n  - EndDate (kế hoạch): 2026-10-30\n- Ngân sách:\n  - Budget: 2.000.000.000\n  - Đã chi: 1.250.000.000\n- Project Manager: Nguyễn Văn A\n- Lần cập nhật gần nhất: 2026-08-03 10:30\n\n2) Tình trạng task chính\n- Đã hoàn thành:\n  - T001 – Implement SSO Login (Backend, Sprint 5, Owner: An, Progress 100%)\n  - T006 – Teams Notification (Backend, Sprint 6, Owner: Hà, Progress 100%)\n- Đang thực hiện:\n  - T002 – Login UI (Frontend, Sprint 5, Owner: Bình, Status: In Progress, Progress 70%, chưa trễ, DueDate: 2026-08-05)\n- Bị chặn:\n  - T003 – Azure Search Integration (Backend, Sprint 5, Owner: Cường, Status: Blocked, RiskLevel: High, Progress 45%, DueDate: 2026-08-02, BlockReason: Waiting Azure permission)\n- Bị trễ:\n  - T004 – Project Dashboard (Frontend, Sprint 5, Owner: Dung, Status: Late, RiskLevel: High, Progress 60%, DueDate: 2026-08-01, ActualHours đã vượt EstimatedHours)\n- Chưa bắt đầu:\n  - T005 – AI Summary API (Backend, Sprint 6, Owner: An, Status: Not Started, RiskLevel: Medium, Progress 0%, StartDate kế hoạch: 2026-08-04, DueDate: 2026-08-10)\n\n3) Rủi ro hiện tại\n- R001 – Azure permission delays\n  - Owner: Cường\n  - Impact: High\n  - Status: Open\n  - Liên quan trực tiếp đến task T003 (Azure Search Integration) đang Blocked.\n- R002 – Frontend dashboard behind schedule\n  - Owner: Dung\n  - Impact: Medium\n  - Status: Open\n  - Liên quan trực tiếp đến task T004 (Project Dashboard) đang Late.\n\n4) Tải công việc của thành viên\n- An (Backend): Capacity 40h/tuần, Allocated 38h (gần full tải, chuẩn bị làm T005).\n- Bình (Frontend): Capacity 40h, Allocated 30h (còn dư, đang làm T002).\n- Cường (Backend): Capacity 40h, Allocated 44h (quá tải, đang giữ task T003 bị Block).\n- Dung (Frontend): Capacity 40h, Allocated 42h (gần quá tải, đang giữ task T004 bị trễ).\n- Hà (Backend): Capacity 40h, Allocated 16h (còn khá nhiều capacity, đã hoàn thành T006).\n\nTóm tắt ngắn: Dự án đang triển khai đúng kế hoạch tổng thể nhưng có 2 điểm nóng: (1) Azure Search Integration bị Block do chậm cấp quyền Azure (rủi ro High, ảnh hưởng backend RAG), (2) Project Dashboard frontend bị trễ và đang là rủi ro High; hai owner Cường và Dung đều đang gần/quá tải, trong khi Hà còn dư tải."
}

////////////////////////////////////////////////////////////////////////
Contract
Post: https://ai.sadec.co/api/contracts/analyze
Phân tích rà soát hợp đồng
body: Multipart form
nhận file (chỉ 1 file)
body:
file: (chọn 1 file)
model_id: UUID

response

{
  "contract_name": "Hợp đồng Cung cấp Dịch vụ Phát triển Phần mềm Hệ thống Quản lý Bán hàng Đa kênh",
  "summary": "Hợp đồng giữa Công ty Cổ phần Thương mại ALPHA (Bên A) và Công ty TNHH Công Nghệ OMEGA (Bên B) về việc Bên B thiết kế, lập trình, kiểm thử và triển khai Hệ thống Quản lý Bán hàng Đa kênh..... Bên B bảo hành hệ thống 12 tháng, hai bên có quy định về phạt chậm tiến độ, phạt chậm thanh toán, quyền đơn phương chấm dứt và cơ chế giải quyết tranh chấp tại VIAC.",
  "clauses": [
    {
      "title": "Phần mở đầu và thông tin các bên",
      "summary": "Xác định căn cứ pháp lý (Bộ luật Dân sự, Luật Thương mại), ngày ký, địa điểm ký, thông tin pháp lý và đại diện của Bên A (Công ty Cổ phần Thương mại ALPHA) và Bên B (Công ty TNHH Công Nghệ OMEGA).",
      "risk": "LOW",
      "recommendation": "Bổ sung rõ số giấy đăng ký kinh doanh và ngày cấp nếu cần, nhưng không bắt buộc."
    },
    {
      "title": "Điều 1: Mục đích và phạm vi công việc",
      "summary": "Quy định mục đích là phát triển Hệ thống Quản lý Bán hàng Đa kênh (Omnichannel Sales Management System)..... Phạm vi bao gồm xây dựng Web App cho quản trị viên và nhân viên bán hàng, Mobile App (iOS & Android) cho khách hàng, tích hợp API thanh toán (VNPay, MoMo) và hệ thống vận chuyển (GHN, Viettel Post).",
      "risk": "MEDIUM",
      "recommendation": "Cần đảm bảo Phụ lục 01 (Đặc tả Yêu cầu SRS) được lập chi tiết, ký kèm và viện dẫn rõ ràng trong hợp đồng....."
    },
    {
      "title": "Điều 2: Thời gian và tiến độ thực hiện",
      "summary": "Tổng thời gian thực hiện là 4 tháng kể từ ngày Bên A thanh toán đợt 1 (tạm ứng). Tiến độ chi tiết: Giai đoạn 1 (tháng 1) hoàn thiện thiết kế UI/UX và kiến trúc hệ thống; Giai đoạn 2 (tháng 2-3) lập trình Backend, Web App và Mobile App; Giai đoạn 3 (tháng 4) kiểm thử UAT, sửa lỗi và triển khai lên server (go-live).",
      "risk": "MEDIUM",
      "recommendation": "Nên bổ sung rõ mốc thời gian bằng ngày/tháng cụ thể gắn với các biên bản bàn giao từng giai đoạn....."
    },
    {
      "title": "Điều 3: Phí dịch vụ và phương thức thanh toán",
      "summary": "Tổng giá trị hợp đồng là 500.000.000 VNĐ, chưa bao gồm 10% VAT. Thanh toán chuyển khoản ngân hàng, chia 3 đợt: Đợt 1: 30% ngay sau khi ký hợp đồng (tạm ứng); Đợt 2: 40% sau khi Bên B bàn giao bản demo cho UAT (cuối Giai đoạn 2); Đợt 3: 30% còn lại trong vòng 7 ngày sau khi ký Biên bản nghiệm thu tổng thể và bàn giao mã nguồn.",
      "risk": "LOW",
      "recommendation": "Bổ sung rõ thông tin tài khoản ngân hàng của Bên B trong hợp đồng hoặc phụ lục....."
    },
    {
      "title": "Điều 4: Bảo mật thông tin và sở hữu trí tuệ",
      "summary": "Hai bên cam kết bảo mật tuyệt đối mọi thông tin, dữ liệu, tài liệu kinh doanh và kỹ thuật nhận được từ bên kia, không tiết lộ cho bên thứ ba nếu không có sự đồng ý bằng văn bản.....",
      "risk": "LOW",
      "recommendation": "Có thể bổ sung quy định về thời hạn bảo mật, phạm vi sử dụng thông tin, và nghĩa vụ hoàn trả/hủy thông tin khi chấm dứt hợp đồng....."
    },
    {
      "title": "Điều 5: Bảo hành và bảo trì",
      "summary": "Bên B bảo hành miễn phí Hệ thống trong 12 tháng kể từ ngày ký Biên bản nghiệm thu tổng thể..... Thời gian phản hồi và xử lý sự cố không vượt quá 24 giờ làm việc kể từ khi nhận được thông báo.",
      "risk": "MEDIUM",
      "recommendation": "Nên làm rõ phạm vi bảo hành (chỉ lỗi do Bên B, không bao gồm lỗi do người dùng, hạ tầng, bên thứ ba), hình thức hỗ trợ (online/onsite), khung giờ làm việc....."
    },
    {
      "title": "Điều 6: Phạt vi phạm và chấm dứt hợp đồng",
      "summary": "Nếu Bên B chậm tiến độ bàn giao quá 10 ngày so với cam kết mà không có lý do chính đáng, Bên B chịu phạt 1% giá trị hợp đồng cho mỗi tuần chậm, tổng mức phạt không vượt quá 8% giá trị hợp đồng..... Hợp đồng có thể bị đơn phương chấm dứt nếu một bên vi phạm nghiêm trọng các điều khoản mà không khắc phục trong 15 ngày kể từ khi nhận thông báo bằng văn bản.",
      "risk": "MEDIUM",
      "recommendation": "Nên định nghĩa rõ thế nào là 'lý do chính đáng' và 'vi phạm nghiêm trọng' để tránh tranh cãi....."
    },
    {
      "title": "Điều 7: Điều khoản chung và giải quyết tranh chấp",
      "summary": "Hai bên cam kết thực hiện nghiêm túc các điều khoản hợp đồng; mọi sửa đổi, bổ sung phải lập thành văn bản và có chữ ký đại diện có thẩm quyền của hai bên (phụ lục hợp đồng)..... Hợp đồng lập thành 4 bản gốc có giá trị pháp lý như nhau, mỗi bên giữ 2 bản.",
      "risk": "LOW",
      "recommendation": "Có thể bổ sung luật áp dụng (ví dụ: pháp luật Việt Nam) nếu hai bên thấy cần; nên ghi rõ ngôn ngữ hợp đồng nếu có bản song ngữ."
    }
  ]
}

//
chat wiht contract
POST: https://ai.sadec.co/api/contracts/chat

body:

 {
  "question": "hợp đồng về dự án phần mềm này có rủi gì cao không",
  "model_id": "31d8f3f4-7a46-4be4-8984-6de1249533ec",
  "contract_id": "f049f044-3d71-4ebf-8990-e92cb82df4f3"

}

response:

{"answer":"## Kết quả\n\nHợp đồng hiện tại tiềm ẩn một số rủi ro khá cao cho Bên A (bên thuê dịch vụ), chủ yếu do:\n\n- Thiếu điều khoản về chậm tiến độ, phạt vi phạm, bồi thường.\n- Thiếu điều khoản về chấm dứt hợp đồng, xử lý khi dự án không đạt yêu cầu.\n- Thiếu điều khoản về bảo hành, bảo trì, hỗ trợ sau khi Go-live.\n- Thiếu quy định rõ về nghiệm thu, tiêu chí đánh giá chất lượng.\n- Thiếu điều khoản về sở hữu trí tuệ, quyền với mã nguồn.\n- Thiếu điều khoản về bảo mật, dữ liệu khách hàng.\n\nDưới đây là phân tích chi tiết dựa trên phần hợp đồng bạn cung cấp.\n\n## Chi tiết\n\n### 1. Tiến độ và chậm tiến độ (Điều 2)\n\n- Hợp đồng chỉ ghi:\n  - “Tổng thời gian thực hiện: 04 tháng kể từ ngày Bên A thanh toán đợt 1 (Tạm ứng).”\n  - Các giai đoạn 1, 2, 3 theo tháng.\n\n**Rủi ro:**\n\n- Không có quy định:\n  - Nếu Bên B chậm tiến độ thì xử lý thế nào.\n  - Có phạt chậm tiến độ hay không.\n  - Bên A có quyền tạm dừng thanh toán, yêu cầu bồi thường, hay chấm dứt hợp đồng không.\n\n=> Nếu Bên B giao trễ, Bên A khó có cơ sở pháp lý để yêu cầu phạt hoặc bồi thường, vì hợp đồng chưa quy định.\n\n### 2. Thanh toán và nghiệm thu (Điều 3)\n\n- 3.1: Tổng giá trị hợp đồng: 500.000.000 VNĐ, chưa gồm VAT.\n- 3.2: Thanh toán 3 đợt:\n  - Đợt 1: 30% ngay sau khi ký (tạm ứng).\n  - Đợt 2: 40% sau khi Bên B bàn giao bản demo cho UAT (cuối Giai đoạn 2).\n  - Đợt 3: 30% còn lại trong 07 ngày sau khi ký Biên bản Nghiệm thu tổng thể và bàn giao mã nguồn.\n\n**Rủi ro:**\n\n- Hợp đồng không nêu:\n  - Tiêu chí nghiệm thu (thế nào là đạt/không đạt).\n  - Quy trình xử lý nếu UAT không đạt (Bên B phải sửa trong bao lâu, nếu sửa không đạt thì sao).\n- Đợt 2: chỉ cần “bàn giao bản demo cho UAT” là được thanh toán 40%, không gắn với điều kiện “demo đạt yêu cầu”.\n- Nếu Bên A đã thanh toán 70% (đợt 1 + 2) mà sản phẩm không đạt yêu cầu, hợp đồng không nói rõ:\n  - Có quyền từ chối nghiệm thu không.\n  - Có quyền yêu cầu hoàn tiền không.\n  - Có quyền chấm dứt hợp đồng không.\n\n=> Rủi ro cho Bên A: đã trả phần lớn tiền nhưng khó từ chối nếu chất lượng không như mong muốn, vì thiếu tiêu chí và quy trình nghiệm thu.\n\n### 3. Quyền với mã nguồn, sở hữu trí tuệ\n\n- Hợp đồng chỉ ghi: “Đợt 3: 30% ... sau khi ký Biên bản Nghiệm thu tổng thể và bàn giao mã nguồn.”\n- Không có điều khoản:\n  - Ai là chủ sở hữu mã nguồn sau khi bàn giao.\n  - Bên B có quyền tái sử dụng, bán cho bên khác hay không.\n  - Bên A có quyền chỉnh sửa, thuê bên khác phát triển tiếp hay không.\n\n**Rủi ro:**\n\n- Nếu sau này phát sinh tranh chấp về quyền sử dụng, sửa đổi, chuyển nhượng phần mềm, hợp đồng hiện tại không có căn cứ rõ ràng để bảo vệ Bên A.\n\n### 4. Bảo hành, bảo trì, hỗ trợ\n\n- Trong phần hợp đồng bạn cung cấp, không có điều khoản:\n  - Thời gian bảo hành (bao lâu, phạm vi gì).\n  - Cách xử lý lỗi sau Go-live (thời gian phản hồi, thời gian sửa lỗi).\n  - Chi phí bảo trì (nếu có).\n\n**Rủi ro:**\n\n- Sau khi Go-live, nếu hệ thống lỗi, Bên A không có cơ sở ràng buộc Bên B phải sửa trong thời gian cụ thể, hoặc miễn phí hay có phí.\n- Dễ dẫn đến tranh chấp khi hệ thống gặp sự cố nhưng hai bên hiểu khác nhau.\n\n### 5. Bảo mật, dữ liệu khách hàng\n\n- Hệ thống là “Hệ thống Quản lý Bán hàng Đa kênh”, có tích hợp thanh toán, vận chuyển, nghĩa là có dữ liệu khách hàng, giao dịch.\n- Hợp đồng không có điều khoản:\n  - Bảo mật thông tin, dữ liệu.\n  - Trách nhiệm nếu lộ dữ liệu.\n  - Cách thức xử lý khi có sự cố bảo mật.\n\n**Rủi ro:**\n\n- Nếu Bên B làm lộ dữ liệu, hoặc nhân sự Bên B sử dụng dữ liệu sai mục đích, Bên A khó có căn cứ cụ thể để yêu cầu bồi thường, vì hợp đồng chưa quy định.\n\n### 6. Chấm dứt hợp đồng, xử lý tranh chấp\n\n- Trong phần hợp đồng bạn cung cấp, chưa thấy:\n  - Điều khoản chấm dứt hợp đồng (khi nào được chấm dứt, hậu quả).\n  - Điều khoản phạt vi phạm, bồi thường thiệt hại.\n  - Cơ chế giải quyết tranh chấp (tòa án, trọng tài, địa điểm).\n\n**Rủi ro:**\n\n- Khi có tranh chấp (chậm tiến độ, chất lượng không đạt, không bàn giao mã nguồn...), hai bên sẽ phải dựa vào luật chung, nhưng hợp đồng không có quy định cụ thể nên bất lợi cho bên yếu thế hơn trong đàm phán.\n\n## Kết luận\n\n- Dựa trên phần hợp đồng bạn cung cấp, mức độ rủi ro cho Bên A là khá cao, chủ yếu vì thiếu các điều khoản bảo vệ quyền lợi Bên A (phạt chậm tiến độ, tiêu chí nghiệm thu, bảo hành, bảo mật, sở hữu mã nguồn, chấm dứt hợp đồng, bồi thường).\n- Nếu bạn là Bên A, nên:\n  - Bổ sung/đàm phán thêm các điều khoản: nghiệm thu, bảo hành, bảo mật, sở hữu trí tuệ, phạt chậm tiến độ, chấm dứt hợp đồng, bồi thường.\n- Nếu bạn là Bên B, cũng nên quy định rõ để tránh tranh chấp về sau.\n\nLưu ý: Phân tích trên chỉ dựa trên phần hợp đồng bạn gửi; nếu hợp đồng đầy đủ có thêm điều khoản khác thì mức độ rủi ro có thể thay đổi."}

///
Lấy danh sách HỢP ĐỒNG (Lấy những hợp đồng đã được phân tích trước đó và lưu db)
GET: https://ai.sadec.co/api/contracts
(có trả về id để khi chat thì truyền id đó cho API Chat lấy đúng hợp đồng đó để chat)


[
  {
    "id": "6183cfee-fc3b-427f-8f2a-57cddd481592",
    "contract_name": "Hợp đồng Cung cấp Dịch vụ Phát triển Phần mềm Hệ thống Quản lý Bán hàng Đa kênh",
    "summary": "Hợp đồng giữa Công ty Cổ phần Thương mại ALPHA (Bên A) và Công ty TNHH Công Nghệ OMEGA (Bên B) về việc Bên B thiết kế, lập trình, kiểm thử và triển khai Hệ thống Quản lý Bán hàng Đa kênh..... Bên B bảo hành hệ thống 12 tháng, hai bên có quy định về phạt chậm tiến độ, phạt chậm thanh toán, quyền đơn phương chấm dứt và cơ chế giải quyết tranh chấp tại VIAC.",
    "created_at": "2026-08-05T02:58:26.519018+00:00"
  },
  {
    "id": "f049f044-3d71-4ebf-8990-e92cb82df4f3",
    "contract_name": "tmpwnwt16zl.pdf",
    "summary": "Hợp đồng giữa Công ty Cổ phần Thương mại ALPHA (Bên A) và Công ty TNHH Công Nghệ OMEGA (Bên B) về việc Bên B cung cấp dịch vụ thiết kế, lập trình, kiểm thử và triển khai Hệ thống Quản lý Bán hàng Đa kênh..... với tổng giá trị 500.000.000 VNĐ (chưa VAT), thanh toán làm 3 đợt theo tiến độ các giai đoạn phát triển phần mềm.",
    "created_at": "2026-08-04T06:47:08.907870+00:00"
  }
]

/////
Lấy thông tin chi tiết một contract
API: GET: https://ai.sadec.co/api/contracts/{id}
ví dụ: https://ai.sadec.co/api/contracts/f049f044-3d71-4ebf-8990-e92cb82df4f3

{
  "id": "f049f044-3d71-4ebf-8990-e92cb82df4f3",
  "contract_name": "tmpwnwt16zl.pdf",
  "summary": "Hợp đồng giữa Công ty Cổ phần Thương mại ALPHA (Bên A) và Công ty TNHH Công Nghệ OMEGA (Bên B) về việc Bên B cung cấp dịch vụ thiết kế, lập trình, kiểm thử và triển khai Hệ thống Quản lý Bán hàng Đa kênh..... với tổng giá trị 500.000.000 VNĐ (chưa VAT), thanh toán làm 3 đợt theo tiến độ các giai đoạn phát triển phần mềm.",
  "clauses": [
    {
      "risk": "LOW",
      "title": "Phần căn cứ pháp lý và nhu cầu hai bên",
      "summary": "Hợp đồng được lập trên cơ sở Bộ luật Dân sự 2015, Luật Thương mại 2005 và nhu cầu, khả năng của hai bên.",
      "recommendation": "Không cần chỉnh sửa, điều khoản chỉ mang tính dẫn chiếu pháp lý chung."
    },
    {
      "risk": "LOW",
      "title": "Thông tin các bên (Bên A và Bên B)",
      "summary": "Quy định thông tin pháp lý và liên hệ của Bên A (Công ty Cổ phần Thương mại ALPHA) và Bên B (Công ty TNHH Công Nghệ OMEGA).....",
      "recommendation": "Kiểm tra lại tính chính xác của tên, mã số thuế, địa chỉ, thông tin đại diện; nếu có sai sót cần chỉnh sửa cho đúng."
    },
    {
      "risk": "MEDIUM",
      "title": "Điều 1: Mục đích và phạm vi công việc",
      "summary": "Xác định dự án là Hệ thống Quản lý Bán hàng Đa kênh. Bên B cung cấp dịch vụ thiết kế, lập trình, kiểm thử và triển khai hệ thống cho Bên A theo tài liệu Đặc tả Yêu cầu (SRS)..... Phạm vi bao gồm (nhưng không giới hạn): xây dựng Web App, Mobile App (iOS & Android), tích hợp API thanh toán (VNPay, MoMo) và hệ thống vận chuyển (GHN, Viettel Post).",
      "recommendation": "Đề nghị làm rõ và hoàn thiện nội dung tài liệu SRS và Phụ lục 01..... Cụm từ “bao gồm nhưng không giới hạn” có thể gây mở rộng phạm vi; nên cân nhắc giới hạn rõ phạm vi để tránh tranh chấp."
    },
    {
      "risk": "MEDIUM",
      "title": "Điều 2: Thời gian và tiến độ thực hiện",
      "summary": "Tổng thời gian thực hiện là 4 tháng kể từ ngày Bên A thanh toán đợt 1 (tạm ứng). Tiến độ chi tiết: Giai đoạn 1 (Tháng 1) thiết kế UI/UX và kiến trúc; Giai đoạn 2 (Tháng 2-3) lập trình Backend, Web App và Mobile App; Giai đoạn 3 (Tháng 4) kiểm thử (UAT), sửa lỗi và Go-live.",
      "recommendation": "Đề nghị bổ sung rõ ngày bắt đầu, ngày kết thúc dự kiến, tiêu chí hoàn thành từng giai đoạn, trách nhiệm khi chậm tiến độ và cơ chế xử lý....."
    },
    {
      "risk": "MEDIUM",
      "title": "Điều 3: Phí dịch vụ và phương thức thanh toán",
      "summary": "Tổng giá trị hợp đồng là 500.000.000 VNĐ, chưa bao gồm 10% VAT. Thanh toán chuyển khoản ngân hàng, chia 3 đợt: Đợt 1: 30% ngay sau khi ký kết (tạm ứng); Đợt 2: 40% sau khi bàn giao bản demo UAT; Đợt 3: 30% còn lại trong vòng 07 ngày sau khi ký Biên bản Nghiệm thu tổng thể và bàn giao mã nguồn.",
      "recommendation": "Đề nghị bổ sung rõ thông tin tài khoản ngân hàng, điều kiện cụ thể để coi là đã bàn giao demo cho UAT, nội dung Biên bản Nghiệm thu tổng thể, và quy định về chậm thanh toán....."
    }
  ]
}

//////////////////////////////////////////////////////////////////////////////////////////
File Statistic
API: POST: https://ai.sadec.co/api/documents/executive-data/sync
API này sẽ trỏ lên sharepoint đã được chỉ định và lấy danh sách file xlsx là các file thống kê đọc và phân tích lưu vào db
body:
{
  "model_id": "31d8f3f4-7a46-4be4-8984-6de1249533ec"
}

reponse: 
{
  "success": 0,
  "total": 1
}
API này không nhất thiết phải gắn vào, hoặc gán nó vào 1 nút trên giao diện cùng feature xem như là thao tác thủ công, bởi vì logic của nó đã được build thành worker và tự động thực hiện sau một khoảng thời gian

////
Chat with file statistic
API: POST
https://ai.sadec.co/api/documents/executive-data/chat

body:
{
  "question": "Chi nhánh nào có doanh thu cao nhất?",
  "model_id": "31d8f3f4-7a46-4be4-8984-6de1249533ec"
}

reponse:
{
  "answer": "Dựa trên dữ liệu doanh thu theo chi nhánh:\n\nTa cộng doanh thu theo từng chi nhánh:\n\n- HCM:\n  - 2026-01: 1.200.000.000\n  - 2026-02: 1.450.000.000  \n  → Tổng: 2.650.000.000\n\n- Ha Noi:\n  - 2026-01: 980.000.000  \n  → Tổng: 980.000.000\n\n- Da Nang:\n  - 2026-02: 520.000.000  \n  → Tổng: 520.000.000\n\n- Can Tho:\n  - 2026-03: 310.000.000  \n  → Tổng: 310.000.000\n\nKết luận: **Chi nhánh HCM có doanh thu cao nhất** với **2.650.000.000**."
}


















