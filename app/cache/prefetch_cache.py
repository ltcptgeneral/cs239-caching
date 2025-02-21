from .cache import BaselineCache

class PrefetchCache(BaselineCache):
    key_relations = None
    
    def __init__(self):
        super()
        self.key_relations = dict()
        
    def put(self, key: str, val: str) -> bool:
        # LRU evict
        evict = False
        if len(self.cache) >= self.limit:
            self.cache.popitem(last = False)
            evict = True
        self.cache[key] = val   
        self.prefetch(key, val)
        
        return evict
    
    def prefetch(self, key: str, val: str) -> bool:
        if len(self.cache) >= self.limit and key in self.key_relations:
            self.cache[self.key_relations[key][0]] = self.key_relations[key][1]
            return True
        return False

    def set_relations(self, key: str, related_key: str, related_val: str):
        self.key_relations[key] = related_key | related_val
        return