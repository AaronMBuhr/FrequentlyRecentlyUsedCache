
#include <unordered_map>
#include <map>
#include <limits>
#include <cmath>
#include <string>
#include <iostream>
#include <optional>

template<typename Key, typename Value>
class FRUCache {
public:
    FRUCache(size_t active_size, size_t ghost_size, double alpha = 1.0, double beta = 1.0)
        : active_size_(active_size), ghost_size_(ghost_size),
          alpha_(alpha), beta_(beta), tick_(0) {}

    std::optional<Value> get(const Key& key) {
        tick_++;
        auto it = active_.find(key);
        if (it != active_.end()) {
            double delta = tick_ - it->second.last_tick;
            it->second.weight += weight_increment(delta);
            it->second.last_tick = tick_;
            return it->second.value;
        }
        auto git = ghost_.find(key);
        if (git != ghost_.end()) {
            double delta = tick_ - git->second.last_tick;
            double new_weight = git->second.weight + weight_increment(delta);
            promote(key, new_weight);
        }
        return std::nullopt;
    }

    void set(const Key& key, const Value& value) {
        tick_++;
        auto it = active_.find(key);
        if (it != active_.end()) {
            double delta = tick_ - it->second.last_tick;
            it->second.weight += weight_increment(delta);
            it->second.last_tick = tick_;
            it->second.value = value;
            return;
        }

        if (active_.size() >= active_size_) {
            auto victim = std::min_element(active_.begin(), active_.end(),
                [](const auto& a, const auto& b) {
                    return a.second.weight < b.second.weight;
                });
            ghost_[victim->first] = {victim->second.weight, victim->second.last_tick};
            active_.erase(victim);
        }

        active_[key] = {value, 1.0, tick_};
        if (ghost_.size() > ghost_size_) {
            auto oldest = std::min_element(ghost_.begin(), ghost_.end(),
                [](const auto& a, const auto& b) {
                    return a.second.last_tick < b.second.last_tick;
                });
            ghost_.erase(oldest);
        }
    }

private:
    struct Entry {
        Value value;
        double weight;
        size_t last_tick;
    };

    struct GhostEntry {
        double weight;
        size_t last_tick;
    };

    double weight_increment(double delta) const {
        return alpha_ * std::pow(delta, beta_);
    }

    void promote(const Key& key, double new_weight) {
        if (active_.size() >= active_size_) {
            auto victim = std::min_element(active_.begin(), active_.end(),
                [](const auto& a, const auto& b) {
                    return a.second.weight < b.second.weight;
                });
            ghost_[victim->first] = {victim->second.weight, victim->second.last_tick};
            active_.erase(victim);
        }
        active_[key] = {Value(), new_weight, tick_};
        ghost_.erase(key);
    }

    std::unordered_map<Key, Entry> active_;
    std::unordered_map<Key, GhostEntry> ghost_;
    size_t active_size_;
    size_t ghost_size_;
    double alpha_;
    double beta_;
    size_t tick_;
};
