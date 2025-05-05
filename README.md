# FRUCache – Frequently-Recently Used Cache

[![Build](https://img.shields.io/github/actions/workflow/status/aaronmbuhr/FrequentlyRecentlyUsedCache/test.yml?branch=main)](https://github.com/aaronmbuhr/FrequentlyRecentlyUsedCache/actions)
[![License](https://img.shields.io/github/license/aaronmbuhr/FrequentlyRecentlyUsedCache)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/aaronmbuhr/FrequentlyRecentlyUsedCache)](https://github.com/aaronmbuhr/FrequentlyRecentlyUsedCache/commits/main)
[![Issues](https://img.shields.io/github/issues/aaronmbuhr/FrequentlyRecentlyUsedCache)](https://github.com/aaronmbuhr/FrequentlyRecentlyUsedCache/issues)

**Author:** Aaron Buhr  
**License:** Apache-2.0 (see [LICENSE](./LICENSE))  
**Status:** Private until publication

---

## 🔍 Overview

FRUCache is a hybrid cache eviction strategy that blends **recency** and **frequency** using a simple, configurable scoring mechanism. It maintains O(1) access efficiency and allows users to tune its behavior to favor recent or frequent accesses—or both.

This repo contains:

- 📘 `fru_cache_technical_explainer.md`: In-depth design and comparison
- 🐍 `fru_cache.py`: Python implementation
- 💠 `fru_cache.cpp`: C++ implementation
- 🧪 `fru_cache_benchmark.py`: Benchmark comparing FRU with LRU
- 📊 `fru_vs_lru_performance.png`: Sample benchmark result

---

## 📐 Scoring Formula

```
weight += \alpha \cdot (tick - last_access)^\beta
```

- `\alpha`: Controls the weight's growth
- `\beta`: Bias toward recency (`0 = LFU`, `1 = balanced`, `>1 = recency`)

---

## ✨ Features

- Configurable LFU/LRU hybrid
- No global decay or background cleanup
- Tracks evicted items for smarter reentry
- Easy-to-extend design

---

## 🔧 Setup

To benchmark in Python:

```bash
python fru_cache_benchmark.py
```

---

## 🛡️ Attribution

If you use this cache or its design, please credit the author:
**Aaron Buhr** – GitHub: [@aaronmbuhr](https://github.com/aaronmbuhr)

---

## 📜 License

Licensed under the Apache License, Version 2.0. See `LICENSE` for details.