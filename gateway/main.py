from fastapi import FastAPI
from gateway.routes import chat

app = FastAPI(title="GPT Gateway (MVP)")
app.include_router(chat.router)

@app.get("/healthz")
def healthz():
    return {"ok": True}
