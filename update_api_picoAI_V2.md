https://ai.sadec.co/api/chat/query

tham số API không thay đổi, thay đổi ở dữ liệu trả về và yêu cầu UI làm theo hướng dẫn

API này đang trả thêm dữ liệu như sau:

{
  "conversation_id": "1af91f54-0c95-4021-bb18-a42b5aa65871",
  "title": "Trình bày cho mình danh sách thiết bị cần triển khai trong kế hoạch lặp đặt thiết bị CNTT",

  "answer": "Dựa trên nội dung Context, tài liệu chỉ nêu chung:\n\n> “Dưới đây là danh sách chi tiết các thiết bị phần cứng bộ phận IT Helpdesk cần tiếp nhận và triển khai.”\n\nTuy nhiên, phần danh sách chi tiết (số lượng, model, thông số) không được cung cấp đầy đủ trong Context, nên không thể liệt kê cụ thể hơn mà không suy diễn.\n\nTrong phạm vi thông tin hiện có, danh sách thiết bị cần triển khai trong kế hoạch lắp đặt thiết bị CNTT gồm:\n\n1. **Thiết bị tại bàn làm việc (cho 150 nhân sự)**\n   - Laptop\n   - PC (máy tính để bàn)\n   - Màn hình\n   - IP Phone\n\n2. **Thiết bị văn phòng chung (Shared Equipments)**\n   - Có đề mục “3.2 Thiết bị văn phòng chung (Shared Equipments)” nhưng Context không nêu rõ loại thiết bị, model hay số lượng, nên không thể liệt kê chi tiết.",

  "chunks": [
    {
      "id": "chunk-uuid-1",
      "source_file": "Ke_Hoach_IT_Helpdesk_Trien_Khai_Thiet_Bi.docx",
      "source_url": "https://sadecco.sharepoint.com/sites/datasource-rag/Shared%20Documents/HR/Ke_Hoach_IT_Helpdesk_Trien_Khai_Thiet_Bi.docx?d=w9cd9dcb0e18249cf825b3db92dd42f31",
      "excerpt": "3. Danh Sách Thiết Bị Cần Triển Khai\n\nDưới đây là danh sách chi tiết các thiết bị phần cứng bộ phận IT Helpdesk cần tiếp nhận và triển khai.",
      "type": "internal"
    },
    {
      "id": "chunk-uuid-2",
      "source_file": "Tai_Lieu_Huong_Dan_Helpdesk_IT.docx",
      "source_url": null,
      "excerpt": "Tài liệu này áp dụng cho toàn thể cán bộ, nhân viên đang làm việc tại văn phòng công ty và sử dụng các trang thiết bị CNTT...",
      "type": "internal"
    }
  ],

  "sources": [
    {
      "source_file": "Ke_Hoach_IT_Helpdesk_Trien_Khai_Thiet_Bi.docx",
      "source_url": "https://sadecco.sharepoint.com/sites/datasource-rag/Shared%20Documents/HR/Ke_Hoach_IT_Helpdesk_Trien_Khai_Thiet_Bi.docx?d=w9cd9dcb0e18249cf825b3db92dd42f31",
      "type": "internal"
    },
    {
      "source_file": "Tai_Lieu_Huong_Dan_Helpdesk_IT.docx",
      "source_url": null,
      "type": "internal"
    }
  ]
}

Nó trả chunk bao gồm các thông tin trong đó excerpt là các chunk được lấy ra và source là danh sách các tài liệu được sử dụng nó sẽ có "source_url", đây là đường dẫn để khi nhấn là sẽ mở file đó

2 thứ này dùng để làm phần hiển thị nguồn khi AI trả lời xong, người dùng xem được nó tham khảo ở đâu để trả lời



/////////////////////////////////////////////////////////////////////////////////////////////



///////////////////////////////////////////////////////////////////////////////////////////


AI hỗ trợ tuyển dụng có bộ API gắn liền với UI như sau

POST: https://ai.sadec.co/api/recruitments
body:
{
  "role_id": 1,
  "title": "đợt tuyển dụng kế toán quý 2 2027",
  "job_description": "Yêu cầu ứng viên có 5 năm kinh nghiệm ở vai trò kế toán"
  
  
}

response
{
  "id": "43d9f5ff-96b0-4980-9fed-b2eab0743e4e",
  "title": "đợt tuyển dụng kế toán quý 2 2027",
  "role_id": 1,
  "job_description": "Yêu cầu ứng viên có 5 năm kinh nghiệm ở vai trò kế toán",
  "status": "draft",
  "created_at": "2026-08-21T02:22:01.862942Z",
  "updated_at": "2026-08-21T02:22:01.862942Z"
}



trong body này "role_id": 1 để lấy được role_id lần trước đã cung cấp API để lấy danh sách role

sau khi tạo sẽ có campaign_id: UUID


/////////////////////////////////////////////


GET: httpS://ai.sadec.co/api/recruitments/list-campaign

API này để lấy danh sách các đợt tuyển dụng đã tạo tức là lấy danh sách campaign
UI: hiển thị bên trái như kiểu conversations

response:
{
  "id": "9999650e-1657-43fc-b179-7e0ccf7b5577",
  "title": "đợt tuyển dụng kế toán quý 3 2026",
  "role_id": 1,
  "job_description": "Yêu cầu có 5 năm kinh nghiệm",
  "status": "draft",
  "total_candidates": 2,
  "created_at": "2026-08-18T02:19:04.696507+00:00",
  "updated_at": "2026-08-18T02:19:04.696507+00:00",
  "candidates": [
    {
      "task_id": "30146fdb-bb0b-4ce0-9d59-8200323d7cfc",
      "file_name": "CV_Middle_Backend_Python.pdf",
      "score": 45,
      "assessment": "Consider"
    },
    {
      "task_id": "41da3329-8f36-41eb-9d16-c668362be9f3",
      "file_name": "CV_Middle_Java_NguyenVanA.pdf",
      "score": 92,
      "assessment": "Strong Hire"
    }
  ]
}

GET: https://ai.sadec.co/api/recruitments/{campaign_id}
API này để hiển thị bên phải danh sách các ứng viên và thông tin chung
khi click 1 campaign khác thì load danh sách ứng viên của campaign đó

response
{
  "id": "9999650e-1657-43fc-b179-7e0ccf7b5577",
  "title": "đợt tuyển dụng kế toán quý 3 2026",
  "role_id": 1,
  "job_description": "Yêu cầu có 5 năm kinh nghiệm",
  "status": "draft",
  "total_candidates": 6,
  "created_at": "2026-08-18T02:19:04.696507+00:00",
  "updated_at": "2026-08-18T02:19:04.696507+00:00",
  "candidates": [
    {
      "task_id": "30146fdb-bb0b-4ce0-9d59-8200323d7cfc",
      "file_name": "CV_Middle_Backend_Python.pdf",
      "score": 45,
      "assessment": "Consider"
    },
    {
      "task_id": "41da3329-8f36-41eb-9d16-c668362be9f3",
      "file_name": "CV_Middle_Java_NguyenVanA.pdf",
      "score": 92,
      "assessment": "Strong Hire"
    },
    {
      "task_id": "b2afa876-6b7a-4177-88e8-d25e191ba365",
      "file_name": "Middle_NET_Developer_CV.pdf",
      "score": 65,
      "assessment": "Consider"
    },
    {
      "task_id": "cc3e0557-6a9a-4454-9941-6821f6cfd822",
      "file_name": "Middle_NET_Developer_CV.pdf",
      "score": 45,
      "assessment": "Reject"
    },
    {
      "task_id": "36ac1c6c-b243-490e-8ab2-44b19db2bada",
      "file_name": "Middle_NET_Developer_CV.pdf",
      "score": 65,
      "assessment": "Consider"
    },
    {
      "task_id": "072f1f51-d9b4-4817-b99b-46d309a778e6",
      "file_name": "NGUYEN HOANG MINH",
      "score": 55,
      "assessment": "Consider"
    }
  ]
}


GET: http://localhost:8000/recruitments/{campaign_id}/candidates/{task_id}

API này để hiển thị chi tiết đầy đủ về ứng viên luôn, khi nhấn thì hiển thị modal để hiển thị các thông tin nnayf

response

{
  "task_id": "30146fdb-bb0b-4ce0-9d59-8200323d7cfc",
  "campaign_id": "9999650e-1657-43fc-b179-7e0ccf7b5577",
  "file_name": "CV_Middle_Backend_Python.pdf",
  "score": 45,
  "assessment": "Consider",
  "reason": "Ứng viên có hơn 2 năm kinh nghiệm backend, đáp ứng yêu cầu về số năm kinh nghiệm nhưng toàn bộ kinh nghiệm tập trung vào Python (FastAPI, Django, Flask), không có kinh nghiệm Java hay Spring Boot/Spring MVC/Spring Data JPA trong CV. Về nền tảng backend, ứng viên có RESTful API, OOP, Microservices, Message Queues (RabbitMQ, Celery), làm việc với PostgreSQL, MySQL, Redis, MongoDB, Git, Docker, CI/CD, AWS, phù hợp với nhiều yêu cầu chung của JD như API, cơ sở dữ liệu quan hệ/NoSQL, message broker, microservices, Docker. Ứng viên cũng có kinh nghiệm tối ưu hiệu năng truy vấn SQL và viết Unit Test (Pytest), làm việc Agile/Scrum, phối hợp với các team khác. Trình độ học vấn đúng chuyên ngành CNTT. Tuy nhiên, các yêu cầu cốt lõi của vị trí Middle Java Developer như Java, hệ sinh thái Spring, Maven/Gradle, Kafka, Kubernetes, design patterns trong bối cảnh Java không được thể hiện trong CV. Do đó mức độ phù hợp với JD về mặt ngôn ngữ và công nghệ chính còn thấp, dù nền tảng backend và tư duy kỹ thuật khá tốt.",
  "summary": "Ứng viên là backend developer Python với hơn 2 năm kinh nghiệm, nền tảng backend và cơ sở dữ liệu tốt. Tuy nhiên, CV không thể hiện bất kỳ kinh nghiệm thực tế với Java hay Spring Boot. Phù hợp nếu công ty chấp nhận chuyển hướng từ Python sang Java và có thời gian đào tạo, còn nếu yêu cầu Java là bắt buộc thì mức độ đáp ứng chưa cao.",
  "strengths": [
    "Hơn 2 năm kinh nghiệm phát triển backend, thiết kế và tối ưu RESTful API",
    "Kinh nghiệm vững với cơ sở dữ liệu quan hệ (PostgreSQL, MySQL) và NoSQL (Redis, MongoDB), có tối ưu truy vấn SQL",
    "Hiểu và áp dụng OOP, làm việc với kiến trúc Microservices và Message Queues (RabbitMQ, Celery)",
    "Kinh nghiệm DevOps cơ bản: Git, Docker, CI/CD (GitHub Actions), triển khai trên AWS",
    "Đã viết Unit Test (Pytest) và tham gia code review, làm việc theo mô hình Agile/Scrum",
    "Tốt nghiệp đại học chuyên ngành Công nghệ Thông tin, có đồ án liên quan đến hệ thống gợi ý sản phẩm"
  ],
  "weaknesses": [
    "Không có kinh nghiệm Java trong CV, không thể hiện sử dụng ngôn ngữ Java trong dự án thực tế",
    "Không có kinh nghiệm với Spring Boot, Spring MVC, Spring Data JPA hoặc bất kỳ framework thuộc hệ sinh thái Java",
    "Không đề cập đến công cụ build Java như Maven, Gradle",
    "Không thể hiện kinh nghiệm với Kafka, Kubernetes, hoặc các công cụ container orchestration khác",
    "Kiến thức về Design Patterns, Data Structures và Algorithms không được mô tả chi tiết trong CV",
    "Mức độ đáp ứng các yêu cầu cốt lõi của vị trí Middle Java Developer (ngôn ngữ và framework chính) còn rất hạn chế"
  ],
  "review_result": {
    "score": 45,
    "reason": "Ứng viên có hơn 2 năm kinh nghiệm backend, đáp ứng yêu cầu về số năm kinh nghiệm nhưng toàn bộ kinh nghiệm tập trung vào Python (FastAPI, Django, Flask), không có kinh nghiệm Java hay Spring Boot/Spring MVC/Spring Data JPA trong CV. Về nền tảng backend, ứng viên có RESTful API, OOP, Microservices, Message Queues (RabbitMQ, Celery), làm việc với PostgreSQL, MySQL, Redis, MongoDB, Git, Docker, CI/CD, AWS, phù hợp với nhiều yêu cầu chung của JD như API, cơ sở dữ liệu quan hệ/NoSQL, message broker, microservices, Docker. Ứng viên cũng có kinh nghiệm tối ưu hiệu năng truy vấn SQL và viết Unit Test (Pytest), làm việc Agile/Scrum, phối hợp với các team khác. Trình độ học vấn đúng chuyên ngành CNTT. Tuy nhiên, các yêu cầu cốt lõi của vị trí Middle Java Developer như Java, hệ sinh thái Spring, Maven/Gradle, Kafka, Kubernetes, design patterns trong bối cảnh Java không được thể hiện trong CV. Do đó mức độ phù hợp với JD về mặt ngôn ngữ và công nghệ chính còn thấp, dù nền tảng backend và tư duy kỹ thuật khá tốt.",
    "summary": "Ứng viên là backend developer Python với hơn 2 năm kinh nghiệm, nền tảng backend và cơ sở dữ liệu tốt. Tuy nhiên, CV không thể hiện bất kỳ kinh nghiệm thực tế với Java hay Spring Boot. Phù hợp nếu công ty chấp nhận chuyển hướng từ Python sang Java và có thời gian đào tạo, còn nếu yêu cầu Java là bắt buộc thì mức độ đáp ứng chưa cao.",
    "strengths": [
      "Hơn 2 năm kinh nghiệm phát triển backend, thiết kế và tối ưu RESTful API",
      "Kinh nghiệm vững với cơ sở dữ liệu quan hệ (PostgreSQL, MySQL) và NoSQL (Redis, MongoDB), có tối ưu truy vấn SQL",
      "Hiểu và áp dụng OOP, làm việc với kiến trúc Microservices và Message Queues (RabbitMQ, Celery)",
      "Kinh nghiệm DevOps cơ bản: Git, Docker, CI/CD (GitHub Actions), triển khai trên AWS",
      "Đã viết Unit Test (Pytest) và tham gia code review, làm việc theo mô hình Agile/Scrum",
      "Tốt nghiệp đại học chuyên ngành Công nghệ Thông tin, có đồ án liên quan đến hệ thống gợi ý sản phẩm"
    ],
    "assessment": "Consider",
    "weaknesses": [
      "Không có kinh nghiệm Java trong CV, không thể hiện sử dụng ngôn ngữ Java trong dự án thực tế",
      "Không có kinh nghiệm với Spring Boot, Spring MVC, Spring Data JPA hoặc bất kỳ framework thuộc hệ sinh thái Java",
      "Không đề cập đến công cụ build Java như Maven, Gradle",
      "Không thể hiện kinh nghiệm với Kafka, Kubernetes, hoặc các công cụ container orchestration khác",
      "Kiến thức về Design Patterns, Data Structures và Algorithms không được mô tả chi tiết trong CV",
      "Mức độ đáp ứng các yêu cầu cốt lõi của vị trí Middle Java Developer (ngôn ngữ và framework chính) còn rất hạn chế"
    ]
  }
}

POST: https://ai.sadec.co/api/recruitments/campaign/chat

API chat, API này chat theo campaign, tức là ở mỗi tab Đợt tuyển dụng (campaign), khi bật chat lên nó sẽ trỏ vào dữ liệu CV của toàn Campaign đó

body:
{
    "campaign_id": "9999650e-1657-43fc-b179-7e0ccf7b5577",

    "model_id": "31d8f3f4-7a46-4be4-8984-6de1249533ec",

    "question": "Có ứng viên nào có kinh nghiệm với bất động sản không?"
}

response:

{"campaign_id":"9999650e-1657-43fc-b179-7e0ccf7b5577","answer":"Trong danh sách hiện tại chỉ có **Ứng viên 1 – Nguyễn Văn A**, và CV của ứng viên này không đề cập đến bất kỳ kinh nghiệm nào liên quan đến lĩnh vực **bất động sản**.\n\nCác kinh nghiệm được nêu gồm:\n- Fintech/tài chính cá nhân (TechFin Solutions VN)\n- E-commerce/thương mại điện tử (Startup ABC)\n- Các dự án kỹ thuật về backend, API, chat app\n\nKhông có thông tin nào về làm việc tại công ty bất động sản, dự án quản lý bất động sản, hay sản phẩm liên quan đến real estate."}







POST: http://localhost:8000/recruitments/analyze
body multipart

model_id: UUID
files: list file (5 file )
campaign_id: UUID

API này sau khi update cần truyền thêm campaign_id: UUID
và bỏ đi job_description


Tổng hợp ý tưởng giao diện:


Bố cục tổng thể: Sidebar bên trái đang chọn tab "Tuyển dụng", phần màn hình chính ở bên phải.

Header: Có tiêu đề "Trợ lý tuyển dụng — chấm & xếp hạng CV" cùng với nút Tạo đợt tuyển dụng mới. Khi click vào nút này sẽ hiển thị một Modal (popup) điền thông tin tạo đợt.

Màn hình chính (chia đôi phía dưới):

Bên trái là danh sách các đợt tuyển dụng. môi dòng sẽ có nút dấu + khi nhấn sẽ hiển thị popup để thêm CV cho AI phân tích (API /analyze)

Bên phải là khu vực chi tiết của đợt đó với 2 Tabs:

Tab "Bảng xếp hạng ứng viên": Chứa bảng ứng viên, có thể cuộn ngang nếu màn hình nhỏ (hiển thị hết bảng).

Tab "Chat": Nằm trọn vẹn trong khung giao diện, không bị kéo ngang, có phần nhập tin nhắn (input) ghim cố định ở phía dưới cùng.

Chi tiết ứng viên: Khi bạn nhấn vào bất kỳ một hàng ứng viên nào trong "Bảng xếp hạng", một popup sẽ hiện lên hiển thị thông tin tóm tắt và đánh giá của ứng viên đó.




