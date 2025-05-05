
class FRUCache:
    def __init__(self, active_size=10, ghost_size=20, alpha=1.0, beta=1.0):
        self.active = {}  # key → (value, weight, last_tick)
        self.ghost = {}   # key → (weight, last_tick)
        self.tick = 0
        self.alpha = alpha
        self.beta = beta
        self.active_size = active_size
        self.ghost_size = ghost_size

    def _weight_increment(self, delta):
        return self.alpha * (delta ** self.beta)

    def get(self, key):
        self.tick += 1
        if key in self.active:
            val, weight, last_tick = self.active[key]
            delta = self.tick - last_tick
            new_weight = weight + self._weight_increment(delta)
            self.active[key] = (val, new_weight, self.tick)
            return val
        elif key in self.ghost:
            weight, last_tick = self.ghost[key]
            delta = self.tick - last_tick
            new_weight = weight + self._weight_increment(delta)
            self._promote(key, new_weight)
        return None

    def set(self, key, value):
        self.tick += 1
        if key in self.active:
            _, weight, last_tick = self.active[key]
            delta = self.tick - last_tick
            self.active[key] = (value, weight + self._weight_increment(delta), self.tick)
        else:
            if len(self.active) >= self.active_size:
                victim_key = min(self.active, key=lambda k: self.active[k][1])
                v_val, v_weight, v_tick = self.active[victim_key]
                self.ghost[victim_key] = (v_weight, v_tick)
                del self.active[victim_key]
            self.active[key] = (value, 1.0, self.tick)
            if len(self.ghost) > self.ghost_size:
                lru_key = min(self.ghost, key=lambda k: self.ghost[k][1])
                del self.ghost[lru_key]

    def _promote(self, key, new_weight):
        if len(self.active) >= self.active_size:
            victim_key = min(self.active, key=lambda k: self.active[k][1])
            v_val, v_weight, v_tick = self.active[victim_key]
            self.ghost[victim_key] = (v_weight, v_tick)
            del self.active[victim_key]
        self.active[key] = (None, new_weight, self.tick)
        if key in self.ghost:
            del self.ghost[key]
