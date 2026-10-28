"""Gemini AI service wrapper."""
from __future__ import annotations

import os
from typing import Any

from google import genai

from app.config import GEMINI_API_KEY


def get_gemini_client() -> Any:
    api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Add it to environment or .env")
    return genai.Client(api_key=api_key)


def summarize_macro_context(context: str) -> str:
    """Generate a short AI summary from macro context."""
    try:
        client = get_gemini_client()
        prompt = (
            "Bạn là chuyên gia tài chính. Tóm tắt ngắn gọn và rõ ràng dựa trên bối cảnh sau:\n\n"
            f"{context}\n\n"
            "Trả lời bằng tiếng Việt, tối đa 200 từ."
        )
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return getattr(response, "text", str(response))
    except Exception as exc:
        return f"AI summary unavailable: {exc}"
