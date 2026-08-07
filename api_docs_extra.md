

UPLOAD TÀI LIỆU LÊN SHAREPOINT
các API phụ hỗ trợ lấy danh sách các thông tin cho user chọn

1. API Lấy danh sách các thư mục có trên site sharepoint đang được dùng để chứa các file dữ liệu
API này cung cấp các tham số cho API chính upload, cung cấp các tham số như: 
site_id
drive_id
folder_id

Note: API này mỗi lần mở khá mất thời gian trong khoảng dưới 40s, yêu cầu UI hiển thị hiệu ứng load
API này được gắn để tự load khi mở màn hình upload (modal, popup,..)

Về ý tưởng UI, màn hình upload hiển thị, chờ API này quét sharepoint để lấy thư mục, UI cần hiển thị thư mục như dạng cây, như Folder trên các IDE như visual code, user muốn upload vào thư mục nào, thì nhấn vào thư mục đó, API này sẽ cung cấp các Folder

GET: https://ai.sadec.co/api/documents/sharepoint/folders

response

[
  {
    "id": "sadecco.sharepoint.com,6d179fbd-3968-4a6c-8367-ed05d5f772fb,62d00dd1-e771-40e3-b539-ac36eea6c013",
    "name": "datasource-rag",
    "libraries": [
      {
        "id": "b!vZ8XbWg5bEqDZ-0F1fdy-9EN0GJx5-NAtTmsNu6mwBPSfyBi7pGER506aIrfYypK",
        "name": "Tài liệu",
        "folders": [
          {
            "id": "014VNYPPXUXHXS5XVMCVF2QKD73UTNFPYO",
            "name": "HR",
            "children": [
              {
                "id": "014VNYPPRKXSNW5XQFUJGJVGUNH7PVJMDI",
                "name": "Q3_PlanA01",
                "children": []
              }
            ]
          },
          {
            "id": "014VNYPPUEWRBP47OLHZHLTH44HNEYWD2U",
            "name": "IT",
            "children": []
          },
          {
            "id": "014VNYPPXXS5K2CVX4EVC2HZVI5AENJFIA",
            "name": "Marketting",
            "children": [
              {
                "id": "014VNYPPUHVQWL5BFWNFD2Z6B5N6D43WN4",
                "name": "Arm_Project",
                "children": [
                  {
                    "id": "014VNYPPUF4UEEJR75IFHIURZ6K6CIUCLF",
                    "name": "Arm_customer",
                    "children": []
                  }
                ]
              },
              {
                "id": "014VNYPPXUVKRRQCNGXJALK5LKI4I26HGK",
                "name": "Inix_Project",
                "children": []
              }
            ]
          },
          {
            "id": "014VNYPPUTYHUPSCSZRJGIYL7P2HZZL3GA",
            "name": "Sale",
            "children": []
          }
        ]
      }
    ]
  }
]

2. API load danh sách document_types để lựa chọn trên UI upload
nó cung cấp name để hiển thị và code và để truyền đi

GET: https://ai.sadec.co/api/configs/document-types

response

[
  {
    "code": "CONTRACT",
    "name": "CONTRACT"
  },
  {
    "code": "HELPDESK",
    "name": "file tài liệu helpdesk"
  },
  {
    "code": "CV",
    "name": "Hồ sơ xin việc"
  },
  {
    "code": "RAG_ASK",
    "name": "Hỏi đáp tài liệu"
  },
  {
    "code": "FULL",
    "name": "Tổng hợp"
  }
]

3. API để load danh sách workspace để lựa chọn
GET: https://ai.sadec.co/api/configs/workspaces

response:
[
  {
    "workspace_name": "Data Q&A điều hành",
    "code": "EXECUTIVE_DATA"
  },
  {
    "workspace_name": "Helpdesk HR/IT",
    "code": "HELPDESK"
  },
  {
    "workspace_name": "Hỏi đáp tài liệu",
    "code": "CHAT_RAG"
  },
  {
    "workspace_name": "Rà soát hợp đồng",
    "code": "CONTRACT_ANALYZE"
  },
  {
    "workspace_name": "Theo dõi tiến độ",
    "code": "PROJECT_TRACKING"
  },
  {
    "workspace_name": "Tóm tắt họp",
    "code": "MEETING_SUMMARY"
  },
  {
    "workspace_name": "Trợ lý AI Tổng hợp",
    "code": "GENERAL_ASSISTANT"
  },
  {
    "workspace_name": "Tuyển dụng",
    "code": "REVIEW_CV"
  }
]

4. API load danh sách role

GET: http://localhost:8000/roles

response

[
  {
    "id": 4,
    "name": "CEO",
    "description": "Chief Executive Officer"
  },
  {
    "id": 5,
    "name": "EXECUTIVE",
    "description": "Executive Leadership"
  },
  {
    "id": 1,
    "name": "HR_MANAGER",
    "description": "Human Resources Manager"
  },
  {
    "id": 2,
    "name": "HR_STAFF",
    "description": "Human Resources Staff"
  },
  {
    "id": 3,
    "name": "CFO",
    "description": "Chief Financial Officer"
  }
]











///////
API chính upload

POST: http://ai.sadec.co/api/documents/upload-sharepoint

input: Multipart Form


file: chỉ nhận 1 file
email: str
role: str (ví dụ: HR_MANAGER)
site_id: sadecco.sharepoint.com,6d179fbd-3968-4a6c-8367-ed05d5f772fb,62d00dd1-e771-40e3-b539-ac36eea6c013
drive_id: b!vZ8XbWg5bEqDZ-0F1fdy-9EN0GJx5-NAtTmsNu6mwBPSfyBi7pGER506aIrfYypK
folder_id: 014VNYPPXUXHXS5XVMCVF2QKD73UTNFPYO
document_type: str
workspace_code: str



trong đó các input dưới đây đã có API lấy đủ thông tin đã trình bày ở trên:
site_id:
drive_id:
folder_id:
document_type: str
workspace_code: str
role,

/////
POST: http://localhost:8000/documents/sync
không có tham số đi kèm

API kích hoạt build data sau khi upload thành công, API nên nên đươnc gắn với một button kích hoạt, vì API này chạy khá lâu nên khi kích hoạt nó sẽ trả 200 ngay nếu không có lỗi, luồng sẽ hoàn toàn tự động chạy.



Ý tưởng tổng thể của feature: Khi mở form Upload đồng thời load lên các thư mục lấy được trên sharepoint theo dạng cây, nhấn vào một thư mục muốn upload lên và chọn file, điền các thông tin, nhấn nút upload, khi upload thành công thì nút Build data mới enable

//////////////////////////////////////////////////////////////////////////////////////////////////////////

PHẦN CONFIG
tab: Nguồn dữ liệu và quyền
màn hình Chế độ nguồn dữ liệu theo workspace
API này lấy ra các dữ liệu cần thiết để hiển thị các config theo workspace như trong mockup

Lưu ý trong response có trả ra trường is_active, nếu là false thì workspcace đó không có được config và cứ hiện mờ không cho xóa sửa là được



GET: https://ai.sadec.co/api/configs

[
  {
    "workspace_id": "427e9eda-24bc-427c-802e-151ab3355f6e",
    "workspace_name": "Data Q&A điều hành",
    "data_source_mode": {
      "id": "3e9c0b7f-2bdf-4ba8-b061-abbcafed013e",
      "code": "INTERNAL",
      "name": "Nội bộ"
    },
    "allow_user_override": false,
    "is_active": true
  },
  {
    "workspace_id": "2d507bd6-b289-4503-940d-af337d92d026",
    "workspace_name": "Helpdesk HR/IT",
    "data_source_mode": {
      "id": "3e9c0b7f-2bdf-4ba8-b061-abbcafed013e",
      "code": "INTERNAL",
      "name": "Nội bộ"
    },
    "allow_user_override": true,
    "is_active": true
  },
  {
    "workspace_id": "2307e199-6df3-4476-add5-368267dbef34",
    "workspace_name": "Hỏi đáp tài liệu",
    "data_source_mode": {
      "id": "213075cf-9860-41ad-ac83-8782d6e9bb23",
      "code": "PUBLIC",
      "name": "Public"
    },
    "allow_user_override": true,
    "is_active": false
  },
  {
    "workspace_id": "f8b4e0b5-9ca4-4637-b215-761df2a36a45",
    "workspace_name": "Rà soát hợp đồng",
    "data_source_mode": {
      "id": "213075cf-9860-41ad-ac83-8782d6e9bb23",
      "code": "PUBLIC",
      "name": "Public"
    },
    "allow_user_override": true,
    "is_active": false
  },
  {
    "workspace_id": "b8675766-1424-411c-8d1d-b9a706b4cf72",
    "workspace_name": "Tuyển dụng",
    "data_source_mode": {
      "id": "c8d2b460-66eb-43fd-b7aa-39de64c7d36e",
      "code": "COMBINE",
      "name": "Kết hợp"
    },
    "allow_user_override": true,
    "is_active": true
  }
]

////
API   
GET: https://ai.sadec.co/api/configs/data-source-modes

response

[
  {
    "id": "c8d2b460-66eb-43fd-b7aa-39de64c7d36e",
    "code": "COMBINE",
    "name": "Kết hợp"
  },
  {
    "id": "3e9c0b7f-2bdf-4ba8-b061-abbcafed013e",
    "code": "INTERNAL",
    "name": "Nội bộ"
  },
  {
    "id": "213075cf-9860-41ad-ac83-8782d6e9bb23",
    "code": "PUBLIC",
    "name": "Public"
  }
]
API này để lấy ra mức độ hiển thị trên cột Chế độ nguồn dữ liệu  để người dùng chuyển đổi như trong mockup

///
API 
PUT: https://ai.sadec.co/api/configs/source-mode

body:
{
  "workspace_id": "427e9eda-24bc-427c-802e-151ab3355f6e",
  "data_source_mode_id": "3e9c0b7f-2bdf-4ba8-b061-abbcafed013e"
}

API để update khi người dùng chuyển đổi 

/////
API
PUT: https://ai.sadec.co/api/configs/allow-user-override

body:
{
  "workspace_id":"427e9eda-24bc-427c-802e-151ab3355f6e",
  "allow_user_override":"false"
}

API này để bật tắt nút 
Cho phép user tự đổi trong chat


////// config tab Model & RAG theo Workspace

1.
chúng ta đã có
GET: https://ai.sadec.co/api/configs/workspaces

response:
[
  {
    "workspace_name": "Data Q&A điều hành",
    "code": "EXECUTIVE_DATA"
  },
  {
    "workspace_name": "Helpdesk HR/IT",
    "code": "HELPDESK"
  },
  {
    "workspace_name": "Hỏi đáp tài liệu",
    "code": "CHAT_RAG"
  },
  {
    "workspace_name": "Rà soát hợp đồng",
    "code": "CONTRACT_ANALYZE"
  },
  {
    "workspace_name": "Theo dõi tiến độ",
    "code": "PROJECT_TRACKING"
  },
  {
    "workspace_name": "Tóm tắt họp",
    "code": "MEETING_SUMMARY"
  },
  {
    "workspace_name": "Trợ lý AI Tổng hợp",
    "code": "GENERAL_ASSISTANT"
  },
  {
    "workspace_name": "Tuyển dụng",
    "code": "REVIEW_CV"
  }
]

API này để hiển thị danh sách workspace bên trái
khi nhấn 1 workspace thì gọi API dưới đây để hiển thị config
GET: https://ai.sadec.co/api/workspace-config/{workspace_id}

Note: dữ liệu trả về gồm 2 phần, phần rag có trường is_active, nếu là false thì hiển thị phần rag mờ đi

response:
{
  "workspace": {
    "id": "2307e199-6df3-4476-add5-368267dbef34",
    "name": "Hỏi đáp tài liệu"
  },
  "model": {
    "provider": "openai",
    "model": "gpt-5.1",
    "temperature": 0.2,
    "max_tokens": 2000,
    "mcp_tool": "chưa có\n"
  },
  "rag": {
    "data_source": "sharepoint",
    "chunking": "Theo đoạn",
    "embedding_model": "text-embedding-3-small",
    "top_k": 10,
    "is_active": true
  }
}

////////////////////
API Update

Update model config:
update trường top_k
PUT: https://ai.sadec.co/api/workspace-config/{workspace_id}/rag

body:
{
  "top_k":10
  
}

////////
API update model config



PUT: https://ai.sadec.co/api/workspace-config/{workspace_id}/model

update 2 trường temperature và max_tokens

body:
{
   "temperature": 0.2,

    "max_tokens": 2000
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////


SỬA Module Chat HELPDESK/IT

thay API cũ bằng API dưới đây
POST: https://ai.sadec.co/api/chat/helpdesk/chat

{
  "conversation_id": "1af91f54-0c95-4021-bb18-a42b5aa65871",
  "role_id": 1,
  "question": "Máy tính của tôi bị hỏng",
  "model_id": "31d8f3f4-7a46-4be4-8984-6de1249533ec",
  "mode": "INTERNAL"
}


mode lấy từ API

GET: https://ai.sadec.co/api/configs/data-source-modes

response

[
  {
    "id": "c8d2b460-66eb-43fd-b7aa-39de64c7d36e",
    "code": "COMBINE",
    "name": "Kết hợp"
  },
  {
    "id": "3e9c0b7f-2bdf-4ba8-b061-abbcafed013e",
    "code": "INTERNAL",
    "name": "Nội bộ"
  },
  {
    "id": "213075cf-9860-41ad-ac83-8782d6e9bb23",
    "code": "PUBLIC",
    "name": "Public"
  }
]












