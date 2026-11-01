"""All non-gameplay screens. Each draw function returns a list of
Buttons; main.py owns click handling so no button is decorative:
every button listed here is checked in main.py.
"""
import pygame
from assets import CHARACTERS, CHARACTER_ORDER, draw_character, draw_city_background
from ui_components import Button, panel, draw_text

GOLD = (255, 190, 20)
BLUE = (30, 110, 240)
DARK = (15, 35, 80)
WHITE = (255, 255, 255)


def title_block(surface, w, settings):
    draw_city_background(surface, w, 720, offset=0)
    draw_text(surface, "RUSH RUNNER", (30, 40), size=64, color=(255, 200, 40), bold=True)
    draw_text(surface, "ENDLESS ADVENTURE", (32, 105), size=26, color=WHITE, bold=True)
    draw_text(surface, f"Coins: {settings.data.get('coins', 0)}   Diamonds: {settings.data.get('diamonds', 0)}",
              (30, 145), size=22, color=(255, 230, 140))


def menu_buttons(w, h):
    x, y = 30, 210
    return [
        ("play", Button((x, y, 220, 56), "PLAY", bg=GOLD)),
        ("character", Button((x, y + 70, 220, 48), "CHARACTER", bg=BLUE, fg=WHITE)),
        ("settings", Button((x, y + 130, 220, 48), "SETTINGS", bg=DARK, fg=WHITE)),
        ("highscore", Button((x, y + 190, 220, 48), "HIGH SCORE", bg=DARK, fg=WHITE)),
        ("quit", Button((x, y + 250, 220, 48), "QUIT", bg=(120, 20, 20), fg=WHITE)),
    ]


def character_screen(surface, w, h, index, settings):
    key = CHARACTER_ORDER[index]
    c = CHARACTERS[key]
    panel(surface, pygame.Rect(30, 30, w - 60, h - 120))
    draw_text(surface, "CHARACTER SELECT", (60, 55), size=40, color=GOLD, bold=True)
    for i, k in enumerate(CHARACTER_ORDER):
        col = GOLD if k == key else (80, 110, 160)
        pygame.draw.rect(surface, col, (50, 130 + i * 80, 70, 60), 3, border_radius=10)
        draw_character(surface, k, 85, 175 + i * 80, scale=0.6)
    draw_character(surface, key, w // 2 + 60, 340, scale=1.4)
    draw_text(surface, c["name"], (w // 2 - 40, 430), size=36, color=WHITE, bold=True)
    draw_text(surface, c["desc"], (w // 2 - 40, 475), size=22, color=(200, 210, 230))
    draw_text(surface, f"Speed: {c['speed']}  Health: {c['health']}  Ability: {c['ability']}",
              (w // 2 - 40, 510), size=22, color=(255, 230, 140))
    return [
        ("prev", Button((50, h - 70, 120, 48), "PREV", bg=DARK, fg=WHITE)),
        ("next", Button((190, h - 70, 120, 48), "NEXT", bg=DARK, fg=WHITE)),
        ("select", Button((w - 260, h - 70, 200, 52), "SELECT", bg=GOLD)),
        ("back", Button((w - 260, 40, 110, 40), "BACK", bg=DARK, fg=WHITE, size=22)),
    ]


def settings_screen(surface, w, h, settings, tilt):
    s = settings.s
    panel(surface, pygame.Rect(30, 30, w - 60, h - 120))
    draw_text(surface, "SETTINGS", (60, 55), size=40, color=GOLD, bold=True)
    rows = [
        ("music", f"Music: {'ON' if s['music'] else 'OFF'}"),
        ("sound", f"Sound Effects: {'ON' if s['sound'] else 'OFF'}"),
        ("graphics", f"Graphics Quality: {s['graphics']}"),
        ("control_style", f"Control Style: {s['control_style']}"),
        ("language", f"Language: {s['language']}"),
        ("control_mode", f"Control Mode: {s['control_mode']} (Touch/Tilt/Both)"),
        ("sensitivity", f"Sensitivity: {s['sensitivity']}"),
    ]
    btns = []
    for i, (k, label) in enumerate(rows):
        draw_text(surface, label, (60, 130 + i * 52), size=24, color=WHITE)
        btns.append((k, Button((w - 180, 120 + i * 52, 120, 36), "CHANGE", bg=DARK, fg=WHITE, size=20)))
    tilt_label = "CALIBRATE NOW" if tilt.available else "TILT: NO SENSOR (touch only)"
    btns.append(("calibrate", Button((60, 130 + len(rows) * 52 + 10, 300, 48),
                                     tilt_label, bg=GOLD if tilt.available else DARK,
                                     fg=(20, 20, 20) if tilt.available else WHITE)))
    btns.append(("back", Button((60, h - 70, 160, 48), "BACK", bg=DARK, fg=WHITE)))
    return btns


def pause_buttons(w, h):
    x = w // 2 - 110
    return [
        ("resume", Button((x, 230, 220, 52), "RESUME", bg=(40, 200, 90), fg=WHITE)),
        ("restart", Button((x, 295, 220, 52), "RESTART", bg=BLUE, fg=WHITE)),
        ("settings", Button((x, 360, 220, 52), "SETTINGS", bg=BLUE, fg=WHITE)),
        ("home", Button((x, 425, 220, 52), "HOME", bg=BLUE, fg=WHITE)),
    ]


def result_buttons(w, h, level_complete=False):
    x = w // 2 - 110
    if level_complete:
        return [("home", Button((x, 460, 220, 52), "HOME", bg=BLUE, fg=WHITE)),
                ("next", Button((x, 525, 220, 52), "NEXT", bg=GOLD))]
    return [("restart", Button((x, 460, 220, 52), "RESTART", bg=BLUE, fg=WHITE)),
            ("home", Button((x, 525, 220, 52), "HOME", bg=BLUE, fg=WHITE))]
