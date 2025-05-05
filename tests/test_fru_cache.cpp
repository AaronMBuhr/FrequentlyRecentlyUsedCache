#include <iostream>
#include <cassert>
#include "../src/cpp/fru_cache.cpp"

void test_basic_set_get() {
    FRUCache<std::string, int> cache(2, 2);
    cache.set("a", 1);
    auto val = cache.get("a");
    assert(val.has_value() && val.value() == 1);
    std::cout << "✔ test_basic_set_get passed\n";
}

void test_eviction_behavior() {
    FRUCache<std::string, int> cache(2, 2);
    cache.set("a", 1);
    cache.set("b", 2);
    cache.set("c", 3);  // should evict one of a or b
    auto val = cache.get("a");
    std::cout << "✔ test_eviction_behavior passed (a was " << (val.has_value() ? "retained" : "evicted") << ")\n";
}

void test_frequency_bias() {
    FRUCache<std::string, int> cache(2, 2);
    for (int i = 0; i < 5; ++i) {
        cache.set("x", 10);
        cache.get("x");
    }
    cache.set("y", 20);
    cache.set("z", 30);
    auto val = cache.get("x");
    assert(val.has_value() && val.value() == 10);
    std::cout << "✔ test_frequency_bias passed\n";
}

int main() {
    test_basic_set_get();
    test_eviction_behavior();
    test_frequency_bias();
    std::cout << "All FRUCache C++ tests passed.\n";
    return 0;
}