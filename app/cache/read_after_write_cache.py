from .cache import BaselineCache
from database import get_user_profile

class ReadAfterWriteCache(BaselineCache):
    
    def __init__(self, limit):
        super().__init__( limit )

    def invalidate(self, key: str) -> bool:
        # basic delete invalidation, but after writing, we immediately read the value and add it to the cache
        invalidated = False
        if key in self.cache:
            del self.cache[key]
            invalidated = True
        
        newData = get_user_profile( key )
        self.put( key, newData )

        return invalidated
    