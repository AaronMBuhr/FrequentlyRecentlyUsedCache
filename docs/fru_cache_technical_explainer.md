
# 📘 Technical Explainer: FRU (Frequently-Recently Used) Cache

## 🧠 Concept Summary

The FRU (Frequently-Recently Used) cache is a novel eviction strategy that blends the benefits of both **Least Recently Used (LRU)** and **Least Frequently Used (LFU)** caches using a simple, efficient, and tunable mechanism.

### Key Goals:
- Track both **recency** and **frequency** of accesses.
- Avoid global decay sweeps or complex probabilistic counters.
- Provide **O(1)** performance per access.
- Be **configurable** to favor different access patterns.

---

## ⚙️ How It Works

Each item in the cache maintains:
- A `weight` representing its access priority.
- A `last_access_tick` timestamp.
- A global `tick` counter that increments on every access.

### Access Update Formula:

$$$
weight += \alpha \cdot (tick - last_access_tick)^\beta
$$$

- `\alpha`: Scales total weight.
- `\beta`: Tunes the bias:
  - `\beta = 0`: Pure LFU
  - `\beta = 1`: Linear aging (balance)
  - `\beta > 1`: Stronger recency bias

Items not accessed recently accrue less weight over time, allowing frequently *and* recently accessed items to naturally rise in importance.

---

## 🔄 Cache Structure

- **Active Cache**: Holds the top-N weighted key-value pairs.
- **Ghost Cache**: Tracks weights of recently evicted items (key only).
- When active is full, the lowest-weight item is demoted to ghost.
- On access to a ghost item, it may be promoted back if its weight warrants.

---

## 🧮 Performance and Complexity

| Operation | Complexity |
|-----------|------------|
| Access    | O(1)       |
| Insert    | O(1)       |
| Eviction  | O(n) linear scan (can be optimized with a heap) |

---

## 📌 Advantages

- No need to decay untouched items.
- Simple deterministic scoring.
- Easily tuned to workload characteristics.
- Outperforms LRU and LFU in mixed-access patterns.

---

## 📎 Use Cases

- Web and database caches where both hot and recently popular entries matter.
- Applications with changing access patterns.
- Scenarios needing **configurable** cache behavior.

---

## 🧱 Comparison

| Feature             | LRU | LFU | TinyLFU | ARC | **FRU** |
|---------------------|-----|-----|---------|-----|---------|
| Recency-aware       | ✅  | ❌  | ⚠️      | ✅  | ✅       |
| Frequency-aware     | ❌  | ✅  | ✅      | ✅  | ✅       |
| Adjustable bias     | ❌  | ❌  | ❌      | ⚠️  | ✅       |
| Touch efficiency    | ✅  | ✅  | ✅      | ✅  | ✅       |
| Global decay needed | ❌  | ✅  | ❌      | ❌  | ❌       |
| Complexity          | Low | Low | Medium  | Med | Low-Med  |

---

## 🛠 Future Extensions

- Background normalization for long-running tick counters.
- Optional heap for efficient eviction.
- Time-based expiration.
- Thread-safe implementation.

