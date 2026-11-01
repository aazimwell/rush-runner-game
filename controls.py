"""Touch swipe + keyboard controls.

Swipe rules: a gesture is recognised only after the finger moves
past DEAD_ZONE pixels, and it fires exactly once per touch (no
repeated lane changes while the finger is still held down).
Desktop: LEFT/RIGHT arrows = lanes, UP/SPACE = jump, DOWN = slide.
"""
DEAD_ZONE = 40


class SwipeDetector:
    def __init__(self):
        self.start = None
        self.fired = False

    def touch_down(self, pos):
        self.start = pos
        self.fired = False

    def touch_move(self, pos):
        """Return 'left'/'right'/'up'/'down' once, else None."""
        if self.start is None or self.fired:
            return None
        dx = pos[0] - self.start[0]
        dy = pos[1] - self.start[1]
        if abs(dx) < DEAD_ZONE and abs(dy) < DEAD_ZONE:
            return None
        self.fired = True
        if abs(dx) > abs(dy):
            return "right" if dx > 0 else "left"
        return "down" if dy > 0 else "up"

    def touch_up(self):
        self.start = None
        self.fired = False


KEY_ACTIONS = {
    "left": "left",
    "right": "right",
    "up": "up",
    "down": "down",
}
