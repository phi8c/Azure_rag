API phân tích cuộc họp
POST: https://ai.sadec.co/api/meeting/analyze




body:

{
  "model_id": "31d8f3f4-7a46-4be4-8984-6de1249533ec",
  "transcript": "Team design đã hoàn tất phần thiết kế UI.Nhóm lập trình sẽ tập trung triển khai giao diện trên web/app. Nhóm lập trình sẽ phát triển hệ thống API. Đã thống nhất sử dụng business plan cho cơ sở dữ liệu.Mục tiêu quan trọng trong tuần: hoàn thiện tính năng đăng nhập.Mục tiêu quan trọng trong tuần: hoàn thiện tính năng tạo công việc mới.Có yêu cầu demo và báo cáo vào 5 giờ chiều thứ 6 tuần này.Mọi người cần chủ động triển khai để đảm bảo tiến độ."
}







response:

{
  "summary": "Cuộc họp thống nhất tình trạng hiện tại của dự án: team design đã hoàn tất UI, nhóm lập trình sẽ triển khai giao diện web/app và phát triển API, sử dụng business plan cho cơ sở dữ liệu. Mục tiêu quan trọng trong tuần là hoàn thiện tính năng đăng nhập và tạo công việc mới, với yêu cầu demo và báo cáo vào 5 giờ chiều thứ 6 tuần này, mọi người cần chủ động triển khai để đảm bảo tiến độ.",
  "key_points": [
    "Team design đã hoàn tất phần thiết kế UI.",
    "Nhóm lập trình sẽ triển khai giao diện trên web/app.",
    "Nhóm lập trình sẽ phát triển hệ thống API.",
    "Đã thống nhất sử dụng business plan cho cơ sở dữ liệu.",
    "Mục tiêu quan trọng trong tuần: hoàn thiện tính năng đăng nhập.",
    "Mục tiêu quan trọng trong tuần: hoàn thiện tính năng tạo công việc mới.",
    "Có yêu cầu demo và báo cáo vào 5 giờ chiều thứ 6 tuần này.",
    "Mọi người cần chủ động triển khai để đảm bảo tiến độ."
  ],
  "decisions": [
    "Sử dụng business plan cho cơ sở dữ liệu.",
    "Tập trung hoàn thiện tính năng đăng nhập trong tuần.",
    "Tập trung hoàn thiện tính năng tạo công việc mới trong tuần.",
    "Thực hiện demo và báo cáo vào 5 giờ chiều thứ 6 tuần này."
  ],
  "action_items": [
    {
      "task": "Triển khai giao diện UI trên web/app dựa trên thiết kế đã hoàn tất.",
      "assignee": "Nhóm lập trình",
      "deadline": null
    },
    {
      "task": "Phát triển hệ thống API.",
      "assignee": "Nhóm lập trình",
      "deadline": null
    },
    {
      "task": "Hoàn thiện tính năng đăng nhập.",
      "assignee": null,
      "deadline": "Trong tuần này"
    },
    {
      "task": "Hoàn thiện tính năng tạo công việc mới.",
      "assignee": null,
      "deadline": "Trong tuần này"
    },
    {
      "task": "Chuẩn bị demo và báo cáo.",
      "assignee": null,
      "deadline": "5 giờ chiều thứ 6 tuần này"
    }
  ],
  "risks": [
    "Nguy cơ không đảm bảo tiến độ nếu mọi người không chủ động triển khai."
  ],
  "unresolved_issues": []
}