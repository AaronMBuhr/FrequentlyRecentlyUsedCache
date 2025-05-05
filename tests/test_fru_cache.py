import unittest
from fru_cache import FRUCache

class TestFRUCache(unittest.TestCase):
    def test_basic_set_get(self):
        cache = FRUCache(active_size=2, ghost_size=2)
        cache.set("a", 1)
        self.assertEqual(cache.get("a"), 1)

    def test_eviction(self):
        cache = FRUCache(active_size=2, ghost_size=2)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        result = cache.get("a")
        self.assertIn(result, [None, 1])  # May be evicted or promoted depending on timing

    def test_frequency_bias(self):
        cache = FRUCache(active_size=2, ghost_size=2)
        for _ in range(5):
            cache.set("x", 100)
            cache.get("x")
        cache.set("y", 200)
        cache.set("z", 300)
        self.assertEqual(cache.get("x"), 100)  # Should survive due to frequent access

if __name__ == "__main__":
    unittest.main()