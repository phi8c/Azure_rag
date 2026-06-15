import json

from app.services.llm.llm_factory import (
    LLMFactory
)


class EntityExtractor:

    def __init__(self):

        self.llm = (
            LLMFactory
            .create()
        )

    async def extract(
        self,
        content: str
    ) -> list[dict]:

        prompt = f"""
Phân tích đoạn văn dưới đây.

Trích xuất các entity quan trọng.

Với mỗi entity trả về:

- name
- summary

summary phải mô tả ngắn gọn vai trò,
ý nghĩa hoặc chức năng của entity
trong chính đoạn văn này.

Chỉ trả về JSON.

Ví dụ:

{{
  "entities": [
    {{
      "name": "Redis",
      "summary": "Lưu thông tin phiên làm việc."
    }}
  ]
}}

ĐOẠN VĂN:

{content}
"""

        response = await (
            self.llm.generate(
                prompt
            )
        )

        try:

            parsed = json.loads(
                response
            )

            return parsed.get(
                "entities",
                []
            )

        except Exception as e:

            print(
                "[EntityExtractor]",
                e
            )

            return []