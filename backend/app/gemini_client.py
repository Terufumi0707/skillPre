from __future__ import annotations

from google import genai


class GeminiClient:
    def __init__(self, api_key: str, model: str) -> None:
        self._client = genai.Client(api_key=api_key)
        self._model = model

    def run(self, prompt: str) -> str:
        response = self._client.models.generate_content(model=self._model, contents=prompt)
        return response.text or ""
