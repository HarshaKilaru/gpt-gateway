from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from gateway.core.auth import require_tenant
from gateway.core.ratelimit import limiter
from gateway.core.providers import pick

router = APIRouter(prefix="/v1", tags=["chat"])

class ChatRequest(BaseModel):
    messages: list[dict] = Field(..., description="List of {role, content}")
    model: str | None = Field(None, description="e.g. openai:gpt-4o-mini or mock:any")
    stream: bool = False
    response_format: dict | None = None
    tools: list[dict] | None = None

@router.post("/chat")
async def chat(req: ChatRequest, request: Request, tenant: str = Depends(require_tenant)):
    limiter.check(tenant)
    provider_name, model_name, provider = pick(req.model)
    text, usage = await provider.chat(messages=req.messages, model=model_name, response_format=req.response_format, tools=req.tools, stream=False)
    return {"output": text, "provider": provider_name, "model": model_name, "tenant": tenant, "usage": usage}
