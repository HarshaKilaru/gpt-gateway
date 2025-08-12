from typing import Protocol, Any, Tuple

class Provider(Protocol):
    name: str
    async def chat(self, *, messages: list[dict], model: str, response_format: dict | None = None, tools: list[dict] | None = None, stream: bool = False) -> Tuple[str, dict | None]:
        """Return (text, usage) where usage is a dict like {'input_tokens':..,'output_tokens':..,'cost_usd':..} or None."""
        ...
