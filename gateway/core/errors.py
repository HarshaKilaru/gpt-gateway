from fastapi import HTTPException, status

def unauthorized(msg: str = "Unauthorized"):
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)

def too_many_requests(msg: str = "Rate limit exceeded"):
    return HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=msg)

def bad_request(msg: str = "Bad request"):
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

def upstream_error(msg: str = "Upstream provider error"):
    return HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=msg)
