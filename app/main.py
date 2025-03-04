from fastapi import FastAPI, HTTPException
from database import get_user_ids, get_user_profile, update_user_profile, get_user_friend_ids
from cache.cache import BaselineCache
from cache.prefetch_cache import PrefetchCache
from cache.tiered_cache import TieredCache
from cache.eviction_sieve import SieveCache
from cache.nocache import NoCache
from cache.idealcache import IdealCache
from cache.read_after_write_cache import ReadAfterWriteCache
from config import CACHE_STRATEGY, CACHE_LIMIT, L2_CACHE_LIMIT
from models.models import User
import time

app = FastAPI()

# Initialize cache based on strategy from config.yaml or environment variable
if CACHE_STRATEGY == "Baseline":
    print("Using baseline cache strategy")
    cache = BaselineCache(limit=CACHE_LIMIT)
elif CACHE_STRATEGY == "Prefetch":
    print("Using prefetch cache strategy")
    cache = PrefetchCache(limit=CACHE_LIMIT)
elif CACHE_STRATEGY == "Tiered":
    print("Using tiered cache strategy")
    cache = TieredCache(limit=CACHE_LIMIT, l2_limit=L2_CACHE_LIMIT)
elif CACHE_STRATEGY == "Sieve":
    print("Using sieve cache strategy")
    cache = SieveCache(limit=CACHE_LIMIT)
elif CACHE_STRATEGY == "None":
    print("Using no cache strategy")
    cache = NoCache(limit=CACHE_LIMIT)
elif CACHE_STRATEGY == "Ideal":
    print("Using ideal cache strategy")
    cache = IdealCache(limit=CACHE_LIMIT)
elif CACHE_STRATEGY == "ReadAfterWrite":
    print("Using read-after-write cache strategy")
    cache = ReadAfterWriteCache(limit=CACHE_LIMIT)
else:
    raise ValueError(f"Invalid CACHE_STRATEGY: {CACHE_STRATEGY}")

@app.get("/users")
def fetch_user_ids():
    return {"ids": get_user_ids()}

@app.get("/users_and_friends")
def fetch_user_and_friends():
    return get_user_friend_ids()

@app.get("/user/{user_id}")
def fetch_user_profile(user_id: str):
    """Fetch user profile with caching"""
    start = time.time()
    cached_profile = cache.get(user_id)
    if cached_profile:
        return {"user_id": user_id, "profile": cached_profile, "source": "cache", "time_ms": (time.time() - start) * 1000}

    profile = get_user_profile(user_id)
    time.sleep(10 / 1000) # simulate 10 ms db delay, we do this here instead of the actual db in the ideal cache case
    if profile is None:
        raise HTTPException(status_code=404, detail="User not found")

    cache.put(user_id, profile)  # Store in cache
    return {"user_id": user_id, "profile": profile, "source": "database", "time_ms": (time.time() - start) * 1000}

@app.post("/update_user/")
async def modify_user_profile(user_data : User):
    """Update user profile and refresh cache"""
    user_id=user_data.user_id
    user_dict = user_data.dict()
    
    update_user_profile(user_dict)
    cache.invalidate(user_id)  # Invalidate old cache
    return {"message": "User profile updated successfully"}
