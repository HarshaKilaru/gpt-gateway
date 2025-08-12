import os, httpx
from typing import Tuple

OPENAI_BASE = "https://api.openai.com/v1"

class OpenAIProvider:
    name = "openai"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    async def chat(self, *, messages, model, response_format=None, tools=None, stream=False) -> Tuple[str, dict | None]:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not configured")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.3,
        }
        # If response_format requests JSON, map to OpenAI's response_format where supported
        if response_format and response_format.get("type") == "json_object":
            payload["response_format"] = {"type": "json_object"}

        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(f"{OPENAI_BASE}/chat/completions", headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            text = data["choices"][0]["message"]["content"]
            usage = data.get("usage")
            # Normalize usage keys
            if usage:
                usage = {
                    "input_tokens": usage.get("prompt_tokens"),
                    "output_tokens": usage.get("completion_tokens"),
                    "cost_usd": None,  # cost calc can be added per-model
                }
            return text, usage
