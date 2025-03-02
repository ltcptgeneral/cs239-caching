from .cache import Cache
from database import get_user_profile

class IdealCache(Cache):

    def __init__(self, limit: int):
        pass

    def get(self, key):
        return get_user_profile(key)

    def put(self, key, val):
        return False
    
    def invalidate(self, key):
        return False