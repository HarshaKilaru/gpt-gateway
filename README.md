# GPT Gateway (MVP)

A minimal, provider-agnostic gateway to integrate GPT into any backend via one normalized API.

## Features (MVP)
- `/v1/chat` endpoint (non-streaming) with a unified request/response shape
- Providers: **OpenAI** and **Mock** (for local dev/tests)
- Bearer auth with **tenant keys**
- Simple **per-tenant rate limit** (RPM)
- Tiny **Python** and **Node** SDKs

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...                         # or set in your shell/OS
export GATEWAY_TENANT_KEYS='demo:demo_key'           # comma list: tenant:key
export GATEWAY_DEFAULT_MODEL='openai:gpt-4o-mini'    # optional override
uvicorn gateway.main:app --reload --port 8000
```

### Test it (Mock provider)
```bash
curl -s -X POST http://localhost:8000/v1/chat   -H "Authorization: Bearer demo_key"   -H "Content-Type: application/json"   -d '{ "model": "mock:any", "messages": [{"role":"user","content":"Hello"}] }' | jq
```

### Test it (OpenAI provider)
```bash
# Requires OPENAI_API_KEY set
curl -s -X POST http://localhost:8000/v1/chat   -H "Authorization: Bearer demo_key"   -H "Content-Type: application/json"   -d '{ "model": "openai:gpt-4o-mini", "messages": [{"role":"user","content":"Say hi in 5 words."}] }' | jq
```

## Env Vars
- `OPENAI_API_KEY` – your OpenAI API key
- `GATEWAY_TENANT_KEYS` – comma list: `tenant1:key1,tenant2:key2`
- `GATEWAY_DEFAULT_MODEL` – fallback model (default: `openai:gpt-4o-mini`)
- `GATEWAY_RATE_LIMIT_RPM` – per-tenant requests/minute (default: `60`)

## Structure
```
gateway/
  main.py
  routes/chat.py
  core/{auth.py,config.py,errors.py,ratelimit.py,providers.py}
  adapters/{base.py,openai.py,mock.py}
sdks/
  python/gpt_gateway/__init__.py
  node/src/index.ts
requirements.txt
```

## Notes
- This MVP returns **non-streaming** responses to keep things simple.
- Extend `adapters/` to add more providers (Anthropic, local models, etc.).
- Replace in-memory rate limiting with Redis in a future commit.
