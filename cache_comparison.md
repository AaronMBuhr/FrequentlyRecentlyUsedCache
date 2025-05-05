# 🧠 Cache Algorithm Comparison: FRU vs ARC vs TinyLFU vs LRU

This document compares commonly used cache eviction strategies, highlighting their benefits, drawbacks, and best-fit scenarios. It also offers guidance for benchmarking and evaluating cache behavior under real-world workloads.

---

## 📊 Comparison Table

| Feature                | LRU       | LFU       | ARC        | TinyLFU      | **FRU (FrequentlyRecentlyUsed)** |
|------------------------|-----------|-----------|------------|--------------|------------------------------|
| Recency-sensitive      | ✅        | ❌        | ✅          | ⚠️ Partial   | ✅ (via tick delta)         |
| Frequency-sensitive    | ❌        | ✅        | ✅          | ✅            | ✅ (via weight increment)   |
| Adaptive to workload   | ❌        | ❌        | ✅          | ✅            | ✅ (manual tuning)          |
| Simplicity             | ✅        | ✅        | ❌ Complex | ❌ Medium     | ✅ (clean, intuitive logic) |
| Touch cost             | O(1)      | O(1)      | O(log N)   | O(1)         | O(1)                        |
| Extra memory usage     | Low       | Low       | Medium     | Medium-High  | Medium (ghost cache)        |
| Requires global decay  | ❌        | ✅        | ❌          | ❌            | ❌                          |
| Tuning control         | ❌        | ❌        | ❌ Auto     | ⚠️ Indirect   | ✅ (α and β parameters)     |

---

## 🧩 Best-Use Scenarios

### ✅ FRUCache
- Mixed recency and frequency workloads
- Systems needing predictable, deterministic behavior
- Embedded or low-overhead systems
- Environments where cache behavior needs to be **tuned manually**
- When developers want **full control over eviction tradeoffs**

### ✅ ARC (Adaptive Replacement Cache)
- Highly dynamic workloads where recency/frequency ratios change often
- Systems that need strong hit rates with no tuning
- General-purpose OS-level page caching (e.g. ZFS, IBM DB2)

### ✅ TinyLFU
- Large-scale systems with extreme skew (e.g., web caches, Redis)
- Memory-constrained environments (Count-Min sketch saves space)
- When approximate frequency filtering is acceptable
- Production use with very high throughput (e.g., Caffeine, Memcached)

### ✅ LRU
- Recency-dominated access (e.g., GUI, session caches)
- Systems where eviction cost is negligible
- When simplicity is more important than efficiency

---

## 🧪 Benchmarking & Real-World Testing

To evaluate cache performance under real workloads:

### 🏁 Metrics
- **Hit Rate**: % of accesses served from cache
- **Miss Rate**: Complement of hit rate
- **Eviction Count**: Total number of evictions
- **Latency/Time**: Time to process N accesses
- **Memory Usage**: Overhead of tracking metadata

### 📚 Access Patterns to Simulate
| Pattern           | Description                                    |
|-------------------|------------------------------------------------|
| Uniform Random    | Every key equally likely (rare in practice)    |
| Zipfian (Skewed)  | Few hot keys dominate traffic (web, Redis)     |
| Sliding Window    | Hotset shifts gradually over time              |
| Bursty Reuse      | Items accessed frequently, then go cold        |
| Full Scan + Reuse | Scans followed by repeated reuse               |

### 🔧 How to Simulate Patterns (Python)

#### Zipfian:
```python
import numpy as np
zipf = np.random.zipf(1.2, size=10000) % 1000
```

#### Sliding window:
```python
accesses = [(i % 100) + (step * 100) for step in range(10) for i in range(1000)]
```

---

## 🔬 Where FRU Shines

- Clear, explainable behavior.
- Easily tuned to workload with α and β parameters.
- Handles burstiness and recency shifts well.
- Easier to implement and debug than ARC or TinyLFU.
- No probabilistic counting or sketch overhead.

---

## 🧠 Summary

FRUCache offers a compelling alternative to more complex adaptive policies, especially where transparency, tunability, and deterministic behavior are important.

To truly assess which cache policy is best, simulate **representative access patterns**, and compare hit rate, eviction churn, and runtime costs under controlled conditions.