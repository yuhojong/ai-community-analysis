import os
from openai import AsyncOpenAI
from google import genai
from typing import List, Optional

class LLMService:
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        self.provider = provider.lower()
        self.api_key = api_key
        self.client = None
        self.model = None

    async def _ensure_client(self, db=None):
        if self.client or self.model:
            return

        if not self.api_key:
            if db:
                from .models import SystemConfig
                key_name = "OPENAI_API_KEY" if self.provider == "openai" else "GEMINI_API_KEY"
                self.api_key = await SystemConfig.get_value(db, key_name)

            if not self.api_key:
                self.api_key = os.getenv("OPENAI_API_KEY") if self.provider == "openai" else os.getenv("GEMINI_API_KEY")

        if self.provider == "openai":
            self.client = AsyncOpenAI(api_key=self.api_key)
        elif self.provider == "gemini":
            self.client = genai.Client(api_key=self.api_key)
            self.model = 'gemini-pro'

    async def analyze_content(self, content_list: List[dict], target_lang: str = "ko", db=None) -> str:
        await self._ensure_client(db)
        if not content_list:
            return "분석할 데이터가 없습니다."

        formatted_content = "\n".join([f"- {item['author']}: {item['content']}" for item in content_list])

        prompt = f"""
다음은 커뮤니티에서 수집된 게시글/메시지들입니다.
이 내용들을 바탕으로 주요 동향과 사용자 의견을 요약하고 분석해 주세요.
결과는 반드시 {target_lang} 언어로 작성해 주세요.

수집된 데이터:
{formatted_content}

리포트 형식:
1. 주요 요약
2. 상세 분석 (긍정/부정 여론 포함)
3. 특징적인 키워드 및 주제
"""

        if self.provider == "openai":
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        elif self.provider == "gemini":
            response = await self.client.aio.models.generate_content(model=self.model, contents=prompt)
            return response.text

        return "Unsupported LLM Provider"
