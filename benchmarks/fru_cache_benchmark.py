import time
import random
from collections import OrderedDict
from fru_cache import FRUCache

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def set(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

def benchmark(cache, keys, accesses):
    hit, miss = 0, 0
    start = time.time()
    for key in accesses:
        if cache.get(key) is not None:
            hit += 1
        else:
            miss += 1
            cache.set(key, key)
    elapsed = time.time() - start
    return hit, miss, elapsed

if __name__ == "__main__":
    keys = list(range(1000))
    access_pattern = []

    # Generate mixed recency and frequency pattern
    for _ in range(10000):
        if random.random() < 0.7:
            access_pattern.append(random.choice(range(100)))  # frequent keys
        else:
            access_pattern.append(random.choice(keys))        # random keys

    fru = FRUCache(active_size=100, ghost_size=100, alpha=1.0, beta=1.0)
    lru = LRUCache(100)

    print("Benchmarking FRU...")
    fru_hit, fru_miss, fru_time = benchmark(fru, keys, access_pattern)
    print(f"FRU: Hits={fru_hit}, Misses={fru_miss}, Time={fru_time:.4f}s")

    print("Benchmarking LRU...")
    lru_hit, lru_miss, lru_time = benchmark(lru, keys, access_pattern)
    print(f"LRU: Hits={lru_hit}, Misses={lru_miss}, Time={lru_time:.4f}s")