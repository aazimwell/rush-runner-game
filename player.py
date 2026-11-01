"""Player: 3 lanes, jump, slide, sprite follows the selected character."""
import pygame
from assets import draw_character

LANES = 3


class Player:
    def __init__(self, char_key="robo"):
        self.char_key = char_key
        self.lane = 1  # 0 left, 1 centre, 2 right
        self.x = 0.0   # smoothed lane position, float
        self.jump_t = 0.0
        self.slide_t = 0.0
        self.tick = 0

    @property
    def jumping(self):
        return self.jump_t > 0

    @property
    def sliding(self):
        return self.slide_t > 0

    def move(self, direction):
        if direction == "left":
            self.lane = max(0, self.lane - 1)
        elif direction == "right":
            self.lane = min(LANES - 1, self.lane + 1)
        elif direction == "up" and not self.jumping:
            self.jump_t = 0.55
        elif direction == "down" and not self.sliding:
            self.slide_t = 0.5

    def update(self, dt):
        self.tick += 1
        target = self.lane - 1  # -1, 0, +1
        self.x += (target - self.x) * min(1.0, dt * 14)
        if self.jump_t > 0:
            self.jump_t -= dt
        if self.slide_t > 0:
            self.slide_t -= dt

    def jump_height(self):
        if self.jump_t <= 0:
            return 0
        # parabola: 0 -> peak -> 0 over the jump duration
        p = 1.0 - self.jump_t / 0.55
        return int(110 * (1 - (2 * p - 1) ** 2))

    def draw(self, surface, lane_xs, ground_y):
        x = int(lane_xs[1] + self.x * (lane_xs[2] - lane_xs[1]))
        y = ground_y - self.jump_height()
        scale = 0.9 if self.sliding else 1.0
        draw_character(surface, self.char_key, x, y, scale=scale,
                       running=True, tick=self.tick)
        return pygame.Rect(x - 25, y - 45 - self.jump_height(), 50, 90)
