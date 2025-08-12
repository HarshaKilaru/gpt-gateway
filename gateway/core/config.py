import os
from pydantic import BaseModel

class Settings(BaseModel):
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL: str = os.getenv("GATEWAY_DEFAULT_MODEL", "openai:gpt-4o-mini")
    RATE_LIMIT_RPM: int = int(os.getenv("GATEWAY_RATE_LIMIT_RPM", "60"))
    # "tenant1:key1,tenant2:key2"
    RAW_TENANT_KEYS: str = os.getenv("GATEWAY_TENANT_KEYS", "demo:demo_key")

    @property
    def TENANT_KEYS(self) -> dict[str, str]:
        out: dict[str, str] = {}
        for pair in self.RAW_TENANT_KEYS.split(","):
            pair = pair.strip()
            if not pair: 
                continue
            if ":" not in pair:
                continue
            t, k = pair.split(":", 1)
            out[t.strip()] = k.strip()
        return out

settings = Settings()
