#!/usr/bin/env python3
"""Rush Runner — Endless Adventure. Entry point.

Desktop:  python3 main.py
Android:  Buildozer entry point (see buildozer.spec / README).

Controls (desktop): arrows / WASD lanes+ jump/slide, P pause, Esc back.
Controls (phone): swipe left/right/up/down; tilt if enabled in Settings
and a sensor is present (see sensors.py — UNVERIFIED on a real device
until a device test; touch always works as fallback).
"""
import os
import sys

import pygame

from controls import SwipeDetector
from game import Gameplay
from menu import (BLUE, DARK, GOLD, WHITE, character_screen, menu_buttons,
                  pause_buttons, result_buttons, settings_screen, title_block)
from sensors import TiltSensor
from settings import Settings
from ui_components import Button, draw_text, panel

W, H = 480, 720


def main():
    pygame.init()
    try:
        pygame.mixer.init()
    except Exception:
        pass
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Rush Runner — Endless Adventure")
    clock = pygame.time.Clock()
    settings = Settings()
    tilt = TiltSensor()
    swipe = SwipeDetector()
    state = "menu"
    prev_state = "menu"
    char_index = 0
    from assets import CHARACTER_ORDER
    try:
        char_index = CHARACTER_ORDER.index(settings.data.get("selected_character", "robo"))
    except ValueError:
        char_index = 0
    game = None
    running = True

    def start_game():
        nonlocal game, state
        game = Gameplay(settings, CHARACTER_ORDER[char_index])
        state = "playing"

    def apply_action(action):
        """Apply a player action in gameplay, respecting control mode."""
        if game is None:
            return
        mode = settings.s.get("control_mode", "touch")
        # tilt actions are applied in the update loop, not here
        if action in ("left", "right", "up", "down"):
            game.player.move(action)

    while running:
        dt = clock.tick(60) / 1000.0
        # ---- tilt (edge-triggered, only in playing) ----
        tilt_dir = 0
        if state == "playing" and settings.s.get("control_mode") in ("tilt", "both"):
            if tilt.available and not tilt.enabled:
                tilt.enable()
            tilt_dir = tilt.direction(settings.s.get("sensitivity", "Medium"))
        elif tilt.enabled:
            tilt.disable()

        buttons = []
        if state == "menu":
            title_block(screen, W, settings)
            buttons = menu_buttons(W, H)
            for _, b in buttons:
                b.draw(screen)
        elif state == "character":
            screen.fill((5, 10, 30))
            buttons = character_screen(screen, W, H, char_index, settings)
            for _, b in buttons:
                b.draw(screen)
        elif state == "settings":
            screen.fill((5, 10, 30))
            buttons = settings_screen(screen, W, H, settings, tilt)
            for _, b in buttons:
                b.draw(screen)
        elif state == "highscore":
            screen.fill((5, 10, 30))
            panel(screen, pygame.Rect(30, 100, W - 60, 300))
            draw_text(screen, "HIGH SCORE", (60, 130), size=40, color=GOLD, bold=True)
            draw_text(screen, f"Best score: {settings.data.get('high_score', 0)}", (60, 200), size=28, color=WHITE)
            draw_text(screen, f"Best distance: {settings.data.get('best_distance', 0)} m", (60, 245), size=28, color=WHITE)
            draw_text(screen, f"Coins: {settings.data.get('coins', 0)}", (60, 290), size=28, color=WHITE)
            buttons = [("back", Button((60, 450, 160, 48), "BACK", bg=DARK, fg=WHITE))]
            for _, b in buttons:
                b.draw(screen)
        elif state == "playing" and game is not None:
            game.update(dt, tilt_dir)
            player_rect = game.draw(screen, W, H)
            hit = game.check_collisions(player_rect)
            if hit and hit[0] == "hit":
                settings.record_run(game.score, game.distance, game.coins_run)
                state = "game_over"
            elif game.milestone_hit:
                game.milestone_hit = False
                settings.record_run(game.score, game.distance, game.coins_run)
                game.last_coins_run = game.coins_run  # for the result screen
                game.coins_run = 0  # banked into the total above
                state = "level_complete"
            # HUD
            draw_text(screen, f"Score: {game.score}", (16, 16), size=26, color=WHITE, bold=True)
            draw_text(screen, f"Coins: {game.coins_run}  Dist: {int(game.distance)}m  Speed x{game.speed:.1f}",
                      (16, 48), size=22, color=(255, 230, 140))
            pause_btn = Button((16, H - 64, 64, 48), "||", bg=DARK, fg=WHITE)
            pause_btn.draw(screen)
            buttons = [("pause", pause_btn)]
        elif state == "paused":
            if game is not None:
                game.draw(screen, W, H)
            panel(screen, pygame.Rect(W // 2 - 150, 180, 300, 320))
            draw_text(screen, "PAUSED", (W // 2 - 70, 210), size=40, color=GOLD, bold=True)
            buttons = pause_buttons(W, H)
            for _, b in buttons:
                b.draw(screen)
        elif state == "level_complete" and game is not None:
            screen.fill((5, 10, 30))
            panel(screen, pygame.Rect(40, 90, W - 80, 480))
            draw_text(screen, "LEVEL COMPLETE!", (70, 130), size=38, color=GOLD, bold=True)
            draw_text(screen, f"Score: {game.score}", (70, 200), size=28, color=WHITE)
            draw_text(screen, f"Coins: {getattr(game, 'last_coins_run', game.coins_run)}  Distance: {int(game.distance)}m", (70, 245), size=24, color=WHITE)
            draw_text(screen, "Stars: ***  (3 stars — milestone reached!)", (70, 290), size=24, color=(255, 220, 80))
            buttons = result_buttons(W, H, level_complete=True)
            for _, b in buttons:
                b.draw(screen)
        elif state == "game_over" and game is not None:
            screen.fill((5, 10, 30))
            panel(screen, pygame.Rect(40, 90, W - 80, 480))
            draw_text(screen, "GAME OVER", (90, 130), size=40, color=(255, 80, 80), bold=True)
            draw_text(screen, f"Score: {game.score}", (70, 200), size=28, color=WHITE)
            draw_text(screen, f"Best: {settings.data.get('high_score', 0)}  Coins: {game.coins_run}",
                      (70, 245), size=24, color=WHITE)
            buttons = result_buttons(W, H, level_complete=False)
            for _, b in buttons:
                b.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                swipe.touch_down(event.pos)
                for name, b in buttons:
                    if b.clicked(event):
                        if state == "menu":
                            if name == "play":
                                start_game()
                            elif name == "character":
                                state = "character"
                            elif name == "settings":
                                prev_state, state = "menu", "settings"
                            elif name == "highscore":
                                state = "highscore"
                            elif name == "quit":
                                running = False
                        elif state == "character":
                            from assets import CHARACTER_ORDER as ORDER
                            if name == "prev":
                                char_index = (char_index - 1) % len(ORDER)
                            elif name == "next":
                                char_index = (char_index + 1) % len(ORDER)
                            elif name == "select":
                                settings.data["selected_character"] = ORDER[char_index]
                                from save_manager import save
                                save(settings.data)
                                state = "menu"
                            elif name == "back":
                                state = "menu"
                        elif state == "settings":
                            if name == "back":
                                state = prev_state
                            elif name == "music":
                                settings.toggle("music")
                            elif name == "sound":
                                settings.toggle("sound")
                            elif name == "graphics":
                                settings.cycle("graphics", ["Low", "Medium", "High"])
                            elif name == "control_style":
                                settings.cycle("control_style", ["Touch", "Tilt", "Both"])
                            elif name == "language":
                                settings.cycle("language", ["English", "Bangla"])
                            elif name == "control_mode":
                                settings.cycle("control_mode", ["touch", "tilt", "both"])
                            elif name == "sensitivity":
                                settings.cycle("sensitivity", ["Low", "Medium", "High"])
                            elif name == "calibrate":
                                tilt.calibrate()
                        elif state == "highscore":
                            if name == "back":
                                state = "menu"
                        elif state == "playing":
                            if name == "pause":
                                state = "paused"
                        elif state == "paused":
                            if name == "resume":
                                state = "playing"
                            elif name == "restart":
                                start_game()
                            elif name == "settings":
                                prev_state, state = "paused", "settings"
                            elif name == "home":
                                state = "menu"
                        elif state == "level_complete":
                            if name == "home":
                                state = "menu"
                            elif name == "next":
                                state = "playing"
                        elif state == "game_over":
                            if name == "restart":
                                start_game()
                            elif name == "home":
                                state = "menu"
            elif event.type == pygame.MOUSEMOTION and state == "playing":
                action = swipe.touch_move(event.pos)
                if action:
                    apply_action(action)
            elif event.type == pygame.MOUSEBUTTONUP:
                swipe.touch_up()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "menu" if state != "playing" else "paused"
                elif event.key == pygame.K_p and state == "playing":
                    state = "paused"
                elif state == "playing":
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        apply_action("left")
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        apply_action("right")
                    elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE):
                        apply_action("up")
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        apply_action("down")
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
