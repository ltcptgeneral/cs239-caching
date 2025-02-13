from abc import ABC, abstractmethod

# implements a simple string k-v store, objects should be serialized before putting into the cache
class Cache(ABC):
    @abstractmethod
    def __init__(self, limit: int):
        """Constructor taking in the cache size limit as number of entries"""
        pass

    @abstractmethod
    def get(self, key: str) -> str:
        """Get the value corresponding to key or returns None if there was a cache miss"""
        pass 
    
    @abstractmethod
    def put(self, key: str, val: str) -> bool:
        """Set the value corresponding to key and returns True if an eviction was made"""
        pass

    @abstractmethod
    def invalidate(self, key: str) -> bool:
        """Mark cache item as invalid and returns True if the element was found and invalidated"""
        pass

from collections import OrderedDict

# the baseline cache using Direct Mapping, LRU eviction, and no prefetching
class BaselineCache(Cache):

    limit = None
    cache = None

    def __init__(self, limit: int):
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
        # no need for this since this op appends key-val by default
        # self.cache.move_to_end(key)

        return evict

    def invalidate(self, key: str) -> bool:
        # basic delete invalidation, no (p)refetching
        if key in self.cache:
            del self.cache[key]
            return True
        else:
            return False

if __name__ == "__main__": # basic testing, should never be called when importing
    cache = BaselineCache(10)

    for i in range(10):
        assert cache.put(str(i), str(i+1)) == False
    
    assert len(cache) == 10
    assert cache == OrderedDict({'0': '1', '1': '2', '2': '3', '3': '4', '4': '5', '5': '6', '6': '7', '7': '8', '8': '9', '9': '10'})

    assert cache.get("5") == "6"
    assert cache.get("8") == "9"
    assert cache.get("0") == "1"

    assert len(cache) == 10
    assert cache == OrderedDict({'1': '2', '2': '3', '3': '4', '4': '5', '6': '7', '7': '8', '9': '10', '5': '6', '8': '9', '0': '1'})

    assert cache.get("a") == None
    assert cache.get("b") == None
    assert cache.get("c") == None

    assert cache.put("a", "b") == True
    assert cache.put("b", "c") == True
    assert cache.put("c", "d") == True

    assert len(cache) == 10
    assert cache == OrderedDict({'4': '5', '6': '7', '7': '8', '9': '10', '5': '6', '8': '9', '0': '1', 'a': 'b', 'b' : 'c', 'c': 'd'})

    assert cache.get("c") == "d"
    assert cache.get("b") == "c"
    assert cache.get("a") == "b"

    assert len(cache) == 10
    assert cache == OrderedDict({'4': '5', '6': '7', '7': '8', '9': '10', '5': '6', '8': '9', '0': '1', 'c': 'd', 'b' : 'c', 'a': 'b'})