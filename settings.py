"""Settings wrapper around save_manager. Every setter persists immediately."""
from save_manager import load, save


class Settings:
    def __init__(self):
        self.data = load()

    @property
    def s(self):
        return self.data["settings"]

    def get(self, key, default=None):
        return self.s.get(key, default)

    def set(self, key, value):
        self.s[key] = value
        save(self.data)

    def toggle(self, key):
        self.set(key, not bool(self.s.get(key, False)))

    def cycle(self, key, options):
        cur = self.s.get(key, options[0])
        nxt = options[(options.index(cur) + 1) % len(options)] if cur in options else options[0]
        self.set(key, nxt)
        return nxt

    def add_coins(self, n):
        self.data["coins"] = int(self.data.get("coins", 0)) + int(n)
        save(self.data)

    def record_run(self, score, distance, coins_earned):
        changed = False
        if score > self.data.get("high_score", 0):
            self.data["high_score"] = int(score)
            changed = True
        if distance > self.data.get("best_distance", 0):
            self.data["best_distance"] = int(distance)
            changed = True
        self.data["coins"] = int(self.data.get("coins", 0)) + int(coins_earned)
        save(self.data)
        return changed
