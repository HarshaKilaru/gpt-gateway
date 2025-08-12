import hashlib, time
from typing import Tuple

class MockProvider:
    name = "mock"

    async def chat(self, *, messages, model, response_format=None, tools=None, stream=False) -> Tuple[str, dict | None]:
        # Deterministic reply based on hash of last user message
        last_user = next((m for m in reversed(messages) if m.get("role") == "user"), {"content": ""})
        seed = hashlib.sha1(last_user.get("content","").encode()).hexdigest()[:6]
        text = f"[mock:{model}] reply-{seed} at {int(time.time())}"
        usage = {"input_tokens": max(1, len(last_user.get('content','')) // 4), "output_tokens": len(text)//4, "cost_usd": 0.0}
        return text, usage
