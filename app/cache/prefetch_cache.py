from .cache import Cache
from database import get_user_profile
from collections import OrderedDict
import math

class PrefetchCache(Cache):
    limit = None
    cache = None
    
    def __init__(self, limit):
        super()
        self.limit = limit
        self.cache = OrderedDict()
        
    def __eq__(self, other):
        return self.cache == other
    
    def __len__(self):
        return len(self.cache)

    def get(self, key: str) -> str:
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        else:
            return None
        
    def put(self, key: str, val: str) -> bool:
        # LRU evict
        evict = False
        if len(self.cache) >= self.limit:
            self.cache.popitem(last = False)
            evict = True
        self.cache[key] = val   
        if self.prefetch(val):
            evict = True
        
        return evict
    
    def prefetch(self, profile) -> bool:
        evict = False
        for i in range(math.ceil(self.limit*0.1)):
            if i < len(profile["friends"]):
                data = get_user_profile(profile["friends"][i])
                if len(self.cache) >= self.limit:
                    self.cache.popitem(last = False)
                    evict = True
                self.cache[profile["friends"][i]] = data
            else:
                break
        return evict

    def invalidate(self, key: str) -> bool:
        # basic delete invalidation, no (p)refetching
        if key in self.cache:
            del self.cache[key]
            return True
        else:
            return False
    