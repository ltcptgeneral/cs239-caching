from fastapi import FastAPI, HTTPException
from database import get_user_profile, update_user_profile
from cache.cache import BaselineCache
from cache.prefetch_cache import PrefetchCache
from cache.tiered_cache import TieredCache
from config import CACHE_STRATEGY, CACHE_LIMIT, L2_CACHE_LIMIT
import time

app = FastAPI()

# Initialize cache based on strategy from config.yaml or environment variable
if CACHE_STRATEGY == "Baseline":
    cache = BaselineCache(limit=CACHE_LIMIT)
elif CACHE_STRATEGY == "Prefetch":
    cache = PrefetchCache()
elif CACHE_STRATEGY == "Tiered":
    cache = TieredCache(limit=CACHE_LIMIT, l2_limit=L2_CACHE_LIMIT)
else:
    raise ValueError(f"Invalid CACHE_STRATEGY: {CACHE_STRATEGY}")

@app.get("/user/{user_id}")
def fetch_user_profile(user_id: str):
    """Fetch user profile with caching"""
    start = time.time()
    cached_profile = cache.get(user_id)
    if cached_profile:
        return {"user_id": user_id, "profile": cached_profile, "source": "cache", "time_ms": (time.time() - start) * 1000}

    profile = get_user_profile(user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="User not found")

    cache.put(user_id, profile)  # Store in cache
    return {"user_id": user_id, "profile": profile, "source": "database", "time_ms": (time.time() - start) * 1000}

@app.post("/update_user/")
def modify_user_profile(user_id: str, name: str, followers: int, bio: str, posts: str):
    """Update user profile and refresh cache"""
    update_user_profile(user_id, name, followers, bio, posts)
    cache.invalidate(user_id)  # Invalidate old cache
    return {"message": "User profile updated successfully"}
