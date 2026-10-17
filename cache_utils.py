# cache_utils.py

import redis
import hashlib
import json
import os
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
)


def get_cache_key(query: str) -> str:
    normalized = " ".join(query.lower().split())
    return "query:" + hashlib.sha256(normalized.encode()).hexdigest()


def get_cached_response(query: str):
    try:
        cached = redis_client.get(get_cache_key(query))
        if cached:
            return json.loads(cached)
    except Exception as e:
        print("CACHE GET FAILED:", e)
    return None


def set_cached_response(query: str, response: str, ttl_seconds: int = 604800):
    try:
        redis_client.setex(get_cache_key(query), ttl_seconds, json.dumps(response))
    except Exception as e:
        print("CACHE SET FAILED:", e)