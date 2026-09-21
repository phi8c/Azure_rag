Hiện tại sẽ cung cấp 2 API get để cung cấp thông tin hiển thị còn các phần xử lý đã được bên FastAPI đảm nhận

API get list meeting

GET: https://ai.sadec.co/api/meeting

response:
[
  {
    "id": "b3009fc5-6023-410d-b624-e89000520abc",
    "title": "meeting daily",
    "start_time": "2026-09-15T03:40:00+00:00",
    "end_time": "2026-09-15T04:10:00+00:00"
  }
]


API get detail meeting

GET: https://ai.sadec.co/api/meeting/{meeting_id}

response: (trong đây có trả đầy đủ tất cả các thông tin cần thiết bao gồm cả summary mà model đã đọc và tóm tắt)

{
  "id": "b3009fc5-6023-410d-b624-e89000520abc",
  "event_id": "AAMkAGJiYzkyNDg2LTdhNTgtNDRmYy05ZDg0LTVlNzcyNjU0ZTZhYQBGAAAAAABntFCxT4qURJ3f1cWS0JFtBwCCsvFMRs8ESJmNWcIam_H4AAAAAAENAACCsvFMRs8ESJmNWcIam_H4AABGnYhTAAA=",
  "online_meeting_id": "MSo4NGM5YmZlMC0wYzZlLTQzMWUtODY2NS1mZWEwYzI3ZjA3ODkqMCoqMTk6bWVldGluZ19abVE0T1RFMFpURXROR1UxTnkwME9UQmhMV0ZtWVRZdFpUazROVFF6T0dJME4yWmxAdGhyZWFkLnYy",
  "subject": "meeting daily",
  "body_preview": "________________________________________________________________________________\r\nMicrosoft Teams meeting\r\nJoin: https://teams.microsoft.com/meet/496119491249482?p=Dqox30LtKOEIJCrNdL\r\nMeeting ID: 496 119 491 249 482\r\nPasscode: nb9N9R8V\r\n________________",
  "description": "<html>\r\n<head>\r\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\r\n</head>\r\n<body>\r\n<br>\r\n<div class=\"me-email-text\" lang=\"en-US\" style=\"max-width:1024px; color:#242424; font-family:'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif\">\r\n<div aria-hidden=\"true\" style=\"margin-bottom:24px; overflow:hidden; white-space:nowrap\">\r\n________________________________________________________________________________</div>\r\n<div style=\"margin-bottom:12px\"><span class=\"me-email-text\" style=\"font-size:20px; color:#242424; font-weight:600\">Microsoft Teams meeting</span>\r\n</div>\r\n<div style=\"margin-bottom:6px\"><span class=\"me-email-text\" style=\"font-size:20px; color:#242424; font-weight:600\">Join:\r\n</span><a href=\"https://teams.microsoft.com/meet/496119491249482?p=Dqox30LtKOEIJCrNdL\" id=\"meet_invite_block.action.join_link\" title=\"Meeting join\" aria-label=\"Meeting join\" class=\"me-email-link\" style=\"font-size:20px; text-decoration:underline; color:#5B5FC7\">https://teams.microsoft.com/meet/496119491249482?p=Dqox30LtKOEIJCrNdL</a>\r\n</div>\r\n<div style=\"margin-bottom:6px\"><span class=\"me-email-text-secondary\" style=\"font-size:14px; color:#616161\">Meeting ID:\r\n</span><span class=\"me-email-text\" style=\"font-size:14px; color:#242424\">496 119 491 249 482</span>\r\n</div>\r\n<div style=\"margin-bottom:32px\"><span class=\"me-email-text-secondary\" style=\"font-size:14px; color:#616161\">Passcode:\r\n</span><span class=\"me-email-text\" style=\"font-size:14px; color:#242424\">nb9N9R8V</span>\r\n</div>\r\n<div style=\"margin-bottom:12px; max-width:1024px\">\r\n<hr style=\"border:0; background:#616161; height:1px\">\r\n</div>\r\n<div style=\"margin-bottom:24px\"><a href=\"https://aka.ms/JoinTeamsMeeting?omkt=en-US\" id=\"meet_invite_block.action.help\" class=\"me-email-link\" style=\"font-size:14px; text-decoration:underline; color:#5B5FC7\">Need help?</a>\r\n<span style=\"color:#616161\">|</span> <a href=\"https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZmQ4OTE0ZTEtNGU1Ny00OTBhLWFmYTYtZTk4NTQzOGI0N2Zl%40thread.v2/0?context=%7b%22Tid%22%3a%22858bad56-b0d7-4d5e-94d7-aa0d82eedbe2%22%2c%22Oid%22%3a%2284c9bfe0-0c6e-431e-8665-fea0c27f0789%22%7d\" id=\"meet_invite_block.action.join_link_compatibility\" class=\"me-email-link\" style=\"font-size:14px; text-decoration:underline; color:#5B5FC7\">\r\nSystem reference</a> </div>\r\n<div><span class=\"me-email-text-secondary\" style=\"font-size:14px; color:#616161\">For organizers:\r\n</span><a href=\"https://teams.microsoft.com/meetingOptions/?organizerId=84c9bfe0-0c6e-431e-8665-fea0c27f0789&amp;tenantId=858bad56-b0d7-4d5e-94d7-aa0d82eedbe2&amp;threadId=19_meeting_ZmQ4OTE0ZTEtNGU1Ny00OTBhLWFmYTYtZTk4NTQzOGI0N2Zl@thread.v2&amp;messageId=0&amp;language=en-US\" id=\"meet_invite_block.action.organizer_meet_options\" class=\"me-email-link\" style=\"font-size:14px; text-decoration:underline; color:#5B5FC7\">Meeting\r\n options</a> </div>\r\n<div style=\"margin-top:24px; margin-bottom:6px\"></div>\r\n<div style=\"margin-bottom:24px\"></div>\r\n<div aria-hidden=\"true\" style=\"margin-bottom:24px; overflow:hidden; white-space:nowrap\">\r\n________________________________________________________________________________</div>\r\n</div>\r\n</body>\r\n</html>\r\n",
  "organizer_name": "Phi, Danh Quang @ PICO",
  "organizer_email": "phi.danh@picosolution.asia",
  "start_time": "2026-09-15T03:40:00+00:00",
  "end_time": "2026-09-15T04:10:00+00:00",
  "location": "Microsoft Teams Meeting",
  "web_link": "https://outlook.office365.com/owa/?itemid=AAMkAGJiYzkyNDg2LTdhNTgtNDRmYy05ZDg0LTVlNzcyNjU0ZTZhYQBGAAAAAABntFCxT4qURJ3f1cWS0JFtBwCCsvFMRs8ESJmNWcIam%2BH4AAAAAAENAACCsvFMRs8ESJmNWcIam%2BH4AABGnYhTAAA%3D&exvsurl=1&path=/calendar/item",
  "join_url": "https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZmQ4OTE0ZTEtNGU1Ny00OTBhLWFmYTYtZTk4NTQzOGI0N2Zl%40thread.v2/0?context=%7b%22Tid%22%3a%22858bad56-b0d7-4d5e-94d7-aa0d82eedbe2%22%2c%22Oid%22%3a%2284c9bfe0-0c6e-431e-8665-fea0c27f0789%22%7d",
  "online_meeting_provider": "teamsForBusiness",
  "attendees": [],
  "has_transcript": true,
  "analysis_status": "completed",
  "summary": "Cuộc họp thống nhất việc team design đã hoàn tất phần thiết kế UI, nhóm lập trình sẽ tập trung triển khai giao diện trên web/app và phát triển hệ thống API. Về cơ sở dữ liệu, nhóm chốt sử dụng business plan. Mục tiêu quan trọng trong tuần là hoàn thiện tính năng đăng nhập và tạo công việc mới, để kịp demo và báo cáo vào 5 giờ chiều thứ 6 tuần này. Mọi người được yêu cầu chủ động triển khai đúng tiến độ.",
  "key_points": [
    "Team design đã hoàn tất phần thiết kế UI.",
    "Nhóm lập trình sẽ tập trung triển khai giao diện trên web/app.",
    "Nhóm lập trình sẽ phát triển hệ thống API.",
    "Đã thống nhất sử dụng business plan cho cơ sở dữ liệu.",
    "Mục tiêu quan trọng trong tuần: hoàn thiện tính năng đăng nhập.",
    "Mục tiêu quan trọng trong tuần: hoàn thiện tính năng tạo công việc mới.",
    "Có yêu cầu demo và báo cáo vào 5 giờ chiều thứ 6 tuần này.",
    "Mọi người cần chủ động triển khai để đảm bảo tiến độ."
  ],
  "decisions": [
    "Thống nhất sử dụng business plan cho cơ sở dữ liệu.",
    "Tập trung phát triển giao diện web/app và hệ thống API trong giai đoạn hiện tại.",
    "Mục tiêu tuần này là hoàn thiện tính năng đăng nhập và tạo công việc mới.",
    "Thực hiện demo và báo cáo vào 5 giờ chiều thứ 6 tuần này."
  ],
  "action_items": [
    {
      "task": "Triển khai giao diện trên web/app dựa trên thiết kế UI đã hoàn tất",
      "assignee": null,
      "deadline": "5 giờ chiều thứ 6 tuần này (trước buổi demo/báo cáo)"
    },
    {
      "task": "Phát triển hệ thống API",
      "assignee": null,
      "deadline": "5 giờ chiều thứ 6 tuần này (trước buổi demo/báo cáo)"
    },
    {
      "task": "Hoàn thiện tính năng đăng nhập",
      "assignee": null,
      "deadline": "Trong tuần này, trước 5 giờ chiều thứ 6"
    },
    {
      "task": "Hoàn thiện tính năng tạo công việc mới",
      "assignee": null,
      "deadline": "Trong tuần này, trước 5 giờ chiều thứ 6"
    },
    {
      "task": "Chuẩn bị demo và báo cáo",
      "assignee": null,
      "deadline": "5 giờ chiều thứ 6 tuần này"
    }
  ],
  "risks": [
    "Nguy cơ không kịp hoàn thiện tính năng đăng nhập và tạo công việc mới trước thời hạn demo vào 5 giờ chiều thứ 6 nếu tiến độ không được đảm bảo."
  ],
  "unresolved_issues": [],
  "model_id": "31d8f3f4-7a46-4be4-8984-6de1249533ec",
  "analyzed_at": "2026-09-15T06:23:29.193752+00:00",
  "raw_data": {
    "id": "AAMkAGJiYzkyNDg2LTdhNTgtNDRmYy05ZDg0LTVlNzcyNjU0ZTZhYQBGAAAAAABntFCxT4qURJ3f1cWS0JFtBwCCsvFMRs8ESJmNWcIam_H4AAAAAAENAACCsvFMRs8ESJmNWcIam_H4AABGnYhTAAA=",
    "end": {
      "dateTime": "2026-09-15T04:10:00.0000000",
      "timeZone": "UTC"
    },
    "uid": "040000008200E00074C5B7101A82E00800000000EEA20555C344DD01000000000000000010000000FE7A78BF84361F42B60A30FAF4D47430",
    "body": {
      "content": "<html>\r\n<head>\r\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\r\n</head>\r\n<body>\r\n<br>\r\n<div class=\"me-email-text\" lang=\"en-US\" style=\"max-width:1024px; color:#242424; font-family:'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif\">\r\n<div aria-hidden=\"true\" style=\"margin-bottom:24px; overflow:hidden; white-space:nowrap\">\r\n________________________________________________________________________________</div>\r\n<div style=\"margin-bottom:12px\"><span class=\"me-email-text\" style=\"font-size:20px; color:#242424; font-weight:600\">Microsoft Teams meeting</span>\r\n</div>\r\n<div style=\"margin-bottom:6px\"><span class=\"me-email-text\" style=\"font-size:20px; color:#242424; font-weight:600\">Join:\r\n</span><a href=\"https://teams.microsoft.com/meet/496119491249482?p=Dqox30LtKOEIJCrNdL\" id=\"meet_invite_block.action.join_link\" title=\"Meeting join\" aria-label=\"Meeting join\" class=\"me-email-link\" style=\"font-size:20px; text-decoration:underline; color:#5B5FC7\">https://teams.microsoft.com/meet/496119491249482?p=Dqox30LtKOEIJCrNdL</a>\r\n</div>\r\n<div style=\"margin-bottom:6px\"><span class=\"me-email-text-secondary\" style=\"font-size:14px; color:#616161\">Meeting ID:\r\n</span><span class=\"me-email-text\" style=\"font-size:14px; color:#242424\">496 119 491 249 482</span>\r\n</div>\r\n<div style=\"margin-bottom:32px\"><span class=\"me-email-text-secondary\" style=\"font-size:14px; color:#616161\">Passcode:\r\n</span><span class=\"me-email-text\" style=\"font-size:14px; color:#242424\">nb9N9R8V</span>\r\n</div>\r\n<div style=\"margin-bottom:12px; max-width:1024px\">\r\n<hr style=\"border:0; background:#616161; height:1px\">\r\n</div>\r\n<div style=\"margin-bottom:24px\"><a href=\"https://aka.ms/JoinTeamsMeeting?omkt=en-US\" id=\"meet_invite_block.action.help\" class=\"me-email-link\" style=\"font-size:14px; text-decoration:underline; color:#5B5FC7\">Need help?</a>\r\n<span style=\"color:#616161\">|</span> <a href=\"https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZmQ4OTE0ZTEtNGU1Ny00OTBhLWFmYTYtZTk4NTQzOGI0N2Zl%40thread.v2/0?context=%7b%22Tid%22%3a%22858bad56-b0d7-4d5e-94d7-aa0d82eedbe2%22%2c%22Oid%22%3a%2284c9bfe0-0c6e-431e-8665-fea0c27f0789%22%7d\" id=\"meet_invite_block.action.join_link_compatibility\" class=\"me-email-link\" style=\"font-size:14px; text-decoration:underline; color:#5B5FC7\">\r\nSystem reference</a> </div>\r\n<div><span class=\"me-email-text-secondary\" style=\"font-size:14px; color:#616161\">For organizers:\r\n</span><a href=\"https://teams.microsoft.com/meetingOptions/?organizerId=84c9bfe0-0c6e-431e-8665-fea0c27f0789&amp;tenantId=858bad56-b0d7-4d5e-94d7-aa0d82eedbe2&amp;threadId=19_meeting_ZmQ4OTE0ZTEtNGU1Ny00OTBhLWFmYTYtZTk4NTQzOGI0N2Zl@thread.v2&amp;messageId=0&amp;language=en-US\" id=\"meet_invite_block.action.organizer_meet_options\" class=\"me-email-link\" style=\"font-size:14px; text-decoration:underline; color:#5B5FC7\">Meeting\r\n options</a> </div>\r\n<div style=\"margin-top:24px; margin-bottom:6px\"></div>\r\n<div style=\"margin-bottom:24px\"></div>\r\n<div aria-hidden=\"true\" style=\"margin-bottom:24px; overflow:hidden; white-space:nowrap\">\r\n________________________________________________________________________________</div>\r\n</div>\r\n</body>\r\n</html>\r\n",
      "contentType": "html"
    },
    "type": "singleInstance",
    "start": {
      "dateTime": "2026-09-15T03:40:00.0000000",
      "timeZone": "UTC"
    },
    "showAs": "busy",
    "iCalUId": "040000008200E00074C5B7101A82E00800000000EEA20555C344DD01000000000000000010000000FE7A78BF84361F42B60A30FAF4D47430",
    "isDraft": false,
    "subject": "meeting daily",
    "webLink": "https://outlook.office365.com/owa/?itemid=AAMkAGJiYzkyNDg2LTdhNTgtNDRmYy05ZDg0LTVlNzcyNjU0ZTZhYQBGAAAAAABntFCxT4qURJ3f1cWS0JFtBwCCsvFMRs8ESJmNWcIam%2BH4AAAAAAENAACCsvFMRs8ESJmNWcIam%2BH4AABGnYhTAAA%3D&exvsurl=1&path=/calendar/item",
    "isAllDay": false,
    "location": {
      "uniqueId": "Microsoft Teams Meeting",
      "displayName": "Microsoft Teams Meeting",
      "locationType": "default",
      "uniqueIdType": "private"
    },
    "attendees": [],
    "changeKey": "grLxTEbPBEiZjVnCGpvh+AAARoyDDw==",
    "locations": [
      {
        "addedBy": "",
        "uniqueId": "Microsoft Teams Meeting",
        "displayName": "Microsoft Teams Meeting",
        "locationType": "default",
        "uniqueIdType": "private"
      }
    ],
    "organizer": {
      "emailAddress": {
        "name": "Phi, Danh Quang @ PICO",
        "address": "phi.danh@picosolution.asia"
      }
    },
    "categories": [],
    "importance": "normal",
    "recurrence": null,
    "@odata.etag": "W/\"grLxTEbPBEiZjVnCGpvh+AAARoyDDw==\"",
    "bodyPreview": "________________________________________________________________________________\r\nMicrosoft Teams meeting\r\nJoin: https://teams.microsoft.com/meet/496119491249482?p=Dqox30LtKOEIJCrNdL\r\nMeeting ID: 496 119 491 249 482\r\nPasscode: nb9N9R8V\r\n________________",
    "isCancelled": false,
    "isOrganizer": true,
    "sensitivity": "normal",
    "isReminderOn": true,
    "occurrenceId": null,
    "hideAttendees": false,
    "onlineMeeting": {
      "joinUrl": "https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZmQ4OTE0ZTEtNGU1Ny00OTBhLWFmYTYtZTk4NTQzOGI0N2Zl%40thread.v2/0?context=%7b%22Tid%22%3a%22858bad56-b0d7-4d5e-94d7-aa0d82eedbe2%22%2c%22Oid%22%3a%2284c9bfe0-0c6e-431e-8665-fea0c27f0789%22%7d"
    },
    "transactionId": "localevent:f138a8dc-32a2-19aa-ccad-aa3857903a9b",
    "hasAttachments": false,
    "responseStatus": {
      "time": "0001-01-01T00:00:00Z",
      "response": "organizer"
    },
    "seriesMasterId": null,
    "createdDateTime": "2026-09-15T03:36:02.6694965Z",
    "isOnlineMeeting": true,
    "onlineMeetingUrl": null,
    "responseRequested": true,
    "originalEndTimeZone": "SE Asia Standard Time",
    "lastModifiedDateTime": "2026-09-15T03:38:04.164936Z",
    "allowNewTimeProposals": true,
    "onlineMeetingProvider": "teamsForBusiness",
    "originalStartTimeZone": "SE Asia Standard Time",
    "reminderMinutesBeforeStart": 15
  },
  "transcripts": [
    {
      "id": "3f2fc6d8-790e-445c-89a1-d278f85ab6b4",
      "transcript_id": "ktVizInGAAAAi_B6lATZRTE5Om1lZXRpbmdfWm1RNE9URTBaVEV0TkdVMU55MDBPVEJoTFdGbVlUWXRaVGs0TlRRek9HSTBOMlpsQHRocmVhZC52MqEw2Tw2NzU1ZjA1Yi1mYTc2LTRlZWMtYTIwZC00NTRiM2JiMjk5OWYtMTc4OTQ0MzYzOC1UcmFuc2NyaXB0VjI=",
      "content": "WEBVTT\r\n\r\n00:02:37.137 --> 00:02:50.977\r\n<v Phi, Danh Quang @ PICO>Nền tín đồ team design đã hoàn tất phần thiết kế UI Wax trong phần này, nhóm lập trình sẽ tập trung lực giao diện văn nền bằng quy app và phát triển hệ thống API iPec gần với top.</v>\r\n\r\n00:02:52.857 --> 00:03:03.737\r\n<v Phi, Danh Quang @ PICO>Về cơ sở dữ liệu, chúng ta thống nhất chốt sử dụng business plan, mục tiêu quan trọng nhất trong tuần là hoàn thiện tính năng đăng nhập và tạo công việc mới.</v>\r\n\r\n00:03:04.817 --> 00:03:10.857\r\n<v Phi, Danh Quang @ PICO>Phải chót để thuốc và demo clotte tay báo cáo 5 giờ chiều thứ 6 tuần này.</v>\r\n\r\n00:03:11.697 --> 00:03:14.257\r\n<v Phi, Danh Quang @ PICO>Mọi người chủ động triển khai đúng độ hết.</v>\r\n\r\n",
      "content_type": "text/vtt",
      "created_at_graph": "2026-09-15T03:40:38.257175+00:00",
      "fetched_at": "2026-09-15T06:23:14.642660+00:00"
    }
  ],
  "created_at": "2026-09-15T06:23:11.265300+00:00",
  "updated_at": "2026-09-15T06:23:29.193752+00:00"
}