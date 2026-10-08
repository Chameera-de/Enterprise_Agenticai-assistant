import time
from dataclasses import dataclass

@dataclass
class Bucket:
    tokens: float
    updated: float

class TokenBucket:
    def __init__(self, capacity=20, refill_per_sec=0.5):
        self.capacity, self.refill = capacity, refill_per_sec
        self.buckets: dict[str, Bucket] = {}
    def allow(self, user: str, cost=1) -> bool:
        now=time.time(); b=self.buckets.setdefault(user, Bucket(self.capacity, now))
        b.tokens=min(self.capacity, b.tokens+(now-b.updated)*self.refill); b.updated=now
        if b.tokens < cost: return False
        b.tokens -= cost; return True
