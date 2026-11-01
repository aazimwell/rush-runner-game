"""Obstacles and coins, moving in pseudo-3D: they start small/far
(at the horizon) and grow as they approach the player at the bottom.
Depth t goes 0 (far) -> 1 (at the player)."""
import random
import pygame
from assets import draw_obstacle, draw_coin


class Entity:
    def __init__(self, lane, kind, is_coin=False):
        self.lane = lane
        self.kind = kind
        self.is_coin = is_coin
        self.t = 0.0  # depth

    def update(self, dt, speed):
        self.t += dt * speed * 0.28

    @property
    def dead(self):
        return self.t >= 1.05


class Spawner:
    def __init__(self):
        self.timer = 0.0
        self.rng = random.Random()

    def update(self, dt, speed, entities):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.rng.uniform(0.7, 1.4)
            lane = self.rng.randrange(3)
            if self.rng.random() < 0.35:
                entities.append(Entity(lane, "coin", is_coin=True))
            else:
                entities.append(Entity(lane, self.rng.choice(["barrier", "car"])))
            # occasionally a second coin in another lane
            if self.rng.random() < 0.3:
                entities.append(Entity((lane + 1) % 3, "coin", is_coin=True))


def entity_screen_pos(ent, lane_xs, horizon_y, ground_y):
    """Interpolate x/y/scale by depth, with perspective narrowing."""
    t = ent.t
    # lane x converges towards centre at the horizon
    centre = lane_xs[1]
    lane_x = lane_xs[ent.lane]
    x = centre + (lane_x - centre) * (0.25 + 0.75 * t)
    y = horizon_y + (ground_y - horizon_y) * t
    scale = 0.25 + 0.75 * t
    return x, y, scale


def draw_entity(surface, ent, lane_xs, horizon_y, ground_y):
    x, y, scale = entity_screen_pos(ent, lane_xs, horizon_y, ground_y)
    if ent.is_coin:
        draw_coin(surface, int(x), int(y - 30 * scale), max(4, int(14 * scale)))
        # generous vertical rect so a coin at ground level is actually
        # collectible when the player runs through it (not just above)
        return pygame.Rect(int(x - 20 * scale), int(y - 70 * scale), int(40 * scale), int(70 * scale))
    w, h = int(70 * scale), int(55 * scale)
    draw_obstacle(surface, ent.kind, int(x - w // 2), int(y - h), w, h)
    return pygame.Rect(int(x - w // 2), int(y - h), w, h)
