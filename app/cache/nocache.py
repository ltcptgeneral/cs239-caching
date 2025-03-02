from .cache import Cache

class NoCache(Cache):

    def __init__(self, limit: int):
        pass

    def get(self, key):
        return None

    def put(self, key, val):
        return False
    
    def invalidate(self, key):
        return False