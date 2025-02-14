from cache import BaselineCache
from collections import OrderedDict
import os

class TieredCache(BaselineCache):
    l2_limit = None
    l2_map = None

    def __init__(self, limit, l2_limit = 100):
        super().__init__(limit)
        self.l2_limit = l2_limit
        self.l2_map = OrderedDict()

    def get(self, key):
        # first look in the l1 cache
        s = super().get(key)
        if s != None:
            return s
        else: # on a miss, check the l2 cache mapping
            if key in self.l2_map: # if it is in l2 cache (disk), open the file and return the values
                f = open(self.l2_map[key], "r")
                v = f.read()
                f.close()
                return v
            else: # otherwise its a cache miss and return None
                return None
    
    def put(self, key, val):
        evict = False
        if len(self.cache) >= self.limit:
            if len(self.l2_map) >= self.l2_limit:
                self.l2_map.popitem(last = False)
                evict = True

            k,v = self.cache.popitem(last = False)
            path = f"tiered_cache/{k}"
            self.l2_map[k] = path
            f = open(path, "w+")
            f.write(v)
            f.close()
            
        self.cache[key] = val

        return evict

    def invalidate(self, key: str) -> bool:
        # basic delete invalidation, no (p)refetching
        if key in self.cache:
            del self.cache[key]
            return True
        elif key in self.l2_map:
            os.remove(self.l2_map[key]) # this is so sketchy
            del self.l2_map[key]
            return True
        else:
            return False

if __name__ == "__main__": # basic testing, should never be called when importing
    cache = TieredCache(10)

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

    assert cache.put("a", "b") == False
    assert cache.put("b", "c") == False
    assert cache.put("c", "d") == False

    assert len(cache) == 10
    assert cache == OrderedDict({'4': '5', '6': '7', '7': '8', '9': '10', '5': '6', '8': '9', '0': '1', 'a': 'b', 'b' : 'c', 'c': 'd'})

    assert cache.get("c") == "d"
    assert cache.get("b") == "c"
    assert cache.get("a") == "b"

    assert cache.get("1") == "2"
    assert cache.get("2") == "3"
    assert cache.get("3") == "4"

    assert len(cache) == 10
    assert cache == OrderedDict({'4': '5', '6': '7', '7': '8', '9': '10', '5': '6', '8': '9', '0': '1', 'c': 'd', 'b' : 'c', 'a': 'b'})