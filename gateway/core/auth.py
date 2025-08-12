from fastapi import Request
from gateway.core.config import settings
from gateway.core.errors import unauthorized

# Simple bearer auth: Authorization: Bearer <tenant_key>
def require_tenant(request: Request) -> str:
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        raise unauthorized("Missing bearer token")
    token = auth.split(" ", 1)[1].strip()
    # find tenant by key
    for tenant, key in settings.TENANT_KEYS.items():
        if token == key:
            return tenant
    raise unauthorized("Invalid bearer token")
