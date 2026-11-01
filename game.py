"""Endless-runner gameplay: road, HUD, collisions, milestones.

Milestone: every 1000 m the run pauses at a LEVEL COMPLETE screen;
NEXT resumes the same run at higher speed. A collision ends the run
at the GAME OVER screen. Score = distance + coins * COIN_SCORE.
"""
import pygame
from assets import draw_city_background
from coins import COIN_SCORE
from obstacles import Spawner, draw_entity
from player import Player

MILESTONE = 1000


class Gameplay:
    def __init__(self, settings, char_key):
        self.settings = settings
        self.player = Player(char_key)
        self.entities = []
        self.spawner = Spawner()
        self.score = 0
        self.coins_run = 0
        self.distance = 0
        self.speed = 1.0
        self.level = 1
        self.next_milestone = MILESTONE
        self.over = False
        self.milestone_hit = False

    def reset(self):
        self.__init__(self.settings, self.player.char_key)

    def update(self, dt, tilt_dir=0):
        if tilt_dir:
            self.player.move("left" if tilt_dir < 0 else "right")
        self.player.update(dt)
        # float accumulation: int(dt * 18) would truncate to 0 per frame
        self.distance += dt * 18 * self.speed
        self.score = int(self.distance) + self.coins_run * COIN_SCORE
        self.speed = min(2.6, 1.0 + self.distance / 4000.0)
        self.spawner.update(dt, self.speed, self.entities)
        for e in list(self.entities):
            e.update(dt, self.speed)
            if e.dead:
                self.entities.remove(e)
        if self.distance >= self.next_milestone:
            self.milestone_hit = True
            self.level += 1
            self.next_milestone += MILESTONE

    def check_collisions(self, player_rect):
        """Returns ('coin', entity) / ('hit', entity) / None."""
        for e in list(self.entities):
            # recompute rects in draw step is expensive; use stored rect
            if getattr(e, "rect", None) is None:
                continue
            if player_rect.colliderect(e.rect):
                self.entities.remove(e)
                if e.is_coin:
                    self.coins_run += 1
                    return ("coin", e)
                if not self.player.jumping:
                    self.over = True
                    return ("hit", e)
        return None

    def draw(self, surface, w, h):
        draw_city_background(surface, w, h, offset=self.distance)
        horizon_y, ground_y = int(h * 0.38), int(h * 0.82)
        lane_xs = [w // 2 - 110, w // 2, w // 2 + 110]
        # road: trapezoid from horizon to bottom
        pygame.draw.polygon(surface, (30, 30, 50),
                            [(w // 2 - 40, horizon_y), (w // 2 + 40, horizon_y),
                             (w - 10, h), (10, h)])
        pygame.draw.polygon(surface, (20, 20, 35),
                            [(w // 2 - 10, horizon_y), (w // 2 + 10, horizon_y),
                             (w // 2 + 60, h), (w // 2 - 60, h)])
        # lane dashes
        for i in range(6):
            yy = horizon_y + (h - horizon_y) * i / 6
            pygame.draw.rect(surface, (255, 200, 40), (w // 2 - 3, yy, 6, 18))
        # entities far -> near so near ones draw on top
        for e in sorted(self.entities, key=lambda x: x.t):
            from obstacles import entity_screen_pos
            x, y, scale = entity_screen_pos(e, lane_xs, horizon_y, ground_y)
            e.rect = draw_entity(surface, e, lane_xs, horizon_y, ground_y)
        player_rect = self.player.draw(surface, lane_xs, ground_y)
        return player_rect
