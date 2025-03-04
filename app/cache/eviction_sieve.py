from .cache import Cache

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.visited = False
        self.next = None
        self.prev = None

class SieveCache(Cache):
    def __init__(self, limit: int):
        super().__init__(limit)
        self.limit = limit  # Fix: Store limit properly
        self.cache = {}  # Hash map for O(1) access
        self.head = None
        self.tail = None
        self.hand = None
    
    def print_cache_state(self):
        #print("Current cache state:")
        node = self.head
        if not node:
            #print("Cache is empty.")
            return
        for _ in range(len(self.cache)):
            #print(f"Key: {node.key}, Value: {node.value}, Visited: {node.visited}")
            node = node.next
            if node == self.head:
                break
    
    def get(self, key: str) -> str:
        if key in self.cache:
            node = self.cache[key]
            node.visited = True
            #self.print_cache_state()
            return node.value
        self.print_cache_state()
        return None
    
    def put(self, key: str, val: str) -> bool:
        if key in self.cache:
            node = self.cache[key]
            node.value = val
            node.visited = True
            #self.print_cache_state()
            return False  # No eviction needed
        
        new_node = Node(key, val)
        if len(self.cache) >= self.limit:
            self.evict()
        
        if not self.head:
            self.head = self.tail = new_node
            new_node.next = new_node.prev = new_node
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.tail.next = new_node
            self.head.prev = new_node
            self.tail = new_node
        
        self.cache[key] = new_node
        if not self.hand:
            self.hand = self.head
        #self.print_cache_state()
        return False
    
    def invalidate(self, key: str) -> bool:
        if key in self.cache:
            node = self.cache.pop(key)
            if node == self.head:
                self.head = node.next
            if node == self.tail:
                self.tail = node.prev
            if node.next:
                node.next.prev = node.prev
            if node.prev:
                node.prev.next = node.next
            #self.print_cache_state()
            return True
        return False
    
    def next_hand(self):
        self.hand = self.hand.next if self.hand.next else self.head
    
    def evict(self):
        while self.hand.visited:
            self.hand.visited = False
            self.next_hand()
        obj_to_evict = self.hand
        self.next_hand()
        
        if obj_to_evict == self.head:
            self.head = obj_to_evict.next
        if obj_to_evict == self.tail:
            self.tail = obj_to_evict.prev
        if obj_to_evict.next:
            obj_to_evict.next.prev = obj_to_evict.prev
        if obj_to_evict.prev:
            obj_to_evict.prev.next = obj_to_evict.next
        
        del self.cache[obj_to_evict.key]
        #self.print_cache_state()

# Basic API demo for future testing
if __name__ == "__main__":
    cache = SeiveCache(3)
    cache.put("a", "1")
    cache.put("b", "2")
    cache.put("c", "3")
    cache.get("a")
    cache.put("d", "4")  # Should evict "b"
    assert "b" not in cache.cache, f"Eviction failed, cache contents: {cache.cache.keys()}"
    print("SeiveCache eviction test passed.")
