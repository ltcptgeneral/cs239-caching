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
        self.limit = limit
        self.cache = {}  # Hash map for O(1) access
        self.head = None
        self.tail = None
        self.hand = None  # Pointer for eviction
    
    def invalidate(self, key: str) -> bool:
        """Removes a specific key from cache if it exists."""
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

            return True  # Successfully invalidated

        return False  # Key not found
    
    def get(self, key: str) -> str:
        if key in self.cache:
            node = self.cache[key]
            node.visited = True  # Mark node as accessed
            return node.value
        return None

    def put(self, key: str, val: str) -> bool:
        if key in self.cache:
            node = self.cache[key]
            node.value = val
            node.visited = True
            return False  # No eviction needed
        
        new_node = Node(key, val)
        if len(self.cache) >= self.limit:
            self.evict()
        
        # Insert new node in circular doubly linked list
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
            self.hand = self.head  # Initialize hand pointer
        return False

    def evict(self):
        if not self.hand:
            return  # No elements to evict

        # Find the first unvisited node to evict
        while self.hand.visited:
            self.hand.visited = False  # Reset visited flag
            self.hand = self.hand.next  # Move to next node

        obj_to_evict = self.hand
        self.hand = self.hand.next  # Move hand forward

        # Remove from cache dictionary if exists
        if obj_to_evict.key in self.cache:
            del self.cache[obj_to_evict.key]

        # Evict the node from linked list
        if obj_to_evict == self.head:
            self.head = obj_to_evict.next
        if obj_to_evict == self.tail:
            self.tail = obj_to_evict.prev

        obj_to_evict.prev.next = obj_to_evict.next
        obj_to_evict.next.prev = obj_to_evict.prev

