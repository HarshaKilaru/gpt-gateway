import time
from collections import defaultdict, deque
from gateway.core.errors import too_many_requests
from gateway.core.config import settings

# very simple sliding window RPM limiter per tenant
class RateLimiter:
    def __init__(self, rpm: int):
        self.rpm = rpm
        self._buckets: dict[str, deque[float]] = defaultdict(deque)

    def check(self, tenant: str):
        now = time.time()
        window = 60.0
        dq = self._buckets[tenant]
        # drop old
        while dq and now - dq[0] > window:
            dq.popleft()
        if len(dq) >= self.rpm:
            raise too_many_requests()
        dq.append(now)

limiter = RateLimiter(rpm=settings.RATE_LIMIT_RPM)
