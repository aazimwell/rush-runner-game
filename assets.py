"""Original, programmatically drawn assets — no copyrighted images.

Characters are drawn with pygame primitives (hoodie, head, trousers,
shoes) in distinct palettes, so each selection visibly changes the
player sprite. ``generate_pngs()`` (see generate_assets.py) renders
the same drawings to PNG files for the APK bundle; at runtime the
game draws them directly, so it never depends on a missing file.
"""
import pygame

CHARACTERS = {
    "robo": {
        "name": "Robo Runner", "desc": "A young hero with unlimited energy!",
        "speed": 0.9, "health": 0.8, "ability": "Magnet",
        "hoodie": (20, 20, 30), "accent": (230, 30, 40), "skin": (240, 200, 160),
    },
    "female": {
        "name": "Female Runner", "desc": "Fast, agile and fearless on the track.",
        "speed": 1.0, "health": 0.7, "ability": "Double Jump",
        "hoodie": (120, 30, 140), "accent": (255, 80, 180), "skin": (240, 200, 160),
    },
    "shadow": {
        "name": "Shadow Runner", "desc": "Moves unseen through the neon night.",
        "speed": 0.85, "health": 0.9, "ability": "Shield",
        "hoodie": (30, 30, 40), "accent": (120, 80, 255), "skin": (200, 200, 210),
    },
    "panda": {
        "name": "Panda Runner", "desc": "Slow and steady, impossible to stop.",
        "speed": 0.7, "health": 1.0, "ability": "Extra Health",
        "hoodie": (240, 240, 240), "accent": (20, 20, 20), "skin": (255, 255, 255),
    },
}
CHARACTER_ORDER = ["robo", "female", "shadow", "panda"]


def draw_character(surface, key, x, y, scale=1.0, running=False, tick=0):
    """Draw a runner centred at (x, y). scale 1.0 ~= 90px tall."""
    c = CHARACTERS.get(key, CHARACTERS["robo"])
    s = scale
    w, h = int(50 * s), int(95 * s)
    # shadow
    pygame.draw.ellipse(surface, (0, 0, 0), (x - w // 2, y + h // 2 - 4, w, int(10 * s)))
    leg = int(6 * s) if running and (tick // 6) % 2 else 0
    # legs / trousers
    pygame.draw.rect(surface, (25, 25, 40), (x - int(14 * s), y + int(10 * s), int(12 * s), int(30 * s) + leg))
    pygame.draw.rect(surface, (25, 25, 40), (x + int(2 * s), y + int(10 * s), int(12 * s), int(30 * s) - leg))
    # shoes (red sneakers for Robo; accent for others)
    shoe = c["accent"] if key != "panda" else (20, 20, 20)
    pygame.draw.rect(surface, shoe, (x - int(16 * s), y + int(38 * s) + leg, int(16 * s), int(8 * s)))
    pygame.draw.rect(surface, shoe, (x + int(2 * s), y + int(38 * s) - leg, int(16 * s), int(8 * s)))
    # hoodie / torso
    pygame.draw.rect(surface, c["hoodie"], (x - int(18 * s), y - int(20 * s), int(36 * s), int(32 * s)))
    pygame.draw.rect(surface, c["accent"], (x - int(4 * s), y - int(20 * s), int(8 * s), int(32 * s)))
    # head
    pygame.draw.circle(surface, c["skin"], (x, y - int(32 * s)), int(13 * s))
    pygame.draw.circle(surface, (20, 20, 25), (x, y - int(38 * s)), int(13 * s))  # hair
    if key == "panda":
        pygame.draw.circle(surface, (20, 20, 20), (x - int(8 * s), y - int(36 * s)), int(4 * s))
        pygame.draw.circle(surface, (20, 20, 20), (x + int(8 * s), y - int(36 * s)), int(4 * s))
    return pygame.Rect(x - w // 2, y - int(45 * s), w, h)


def draw_coin(surface, x, y, r=14):
    pygame.draw.circle(surface, (255, 200, 40), (x, y), r)
    pygame.draw.circle(surface, (255, 230, 120), (x, y), r - 4)
    pygame.draw.circle(surface, (200, 140, 0), (x, y), r - 9, 2)


def draw_obstacle(surface, kind, x, y, w, h):
    if kind == "barrier":
        pygame.draw.rect(surface, (255, 120, 30), (x, y, w, h))
        pygame.draw.rect(surface, (20, 20, 30), (x, y, w, 8))
        pygame.draw.rect(surface, (255, 255, 255), (x + 6, y + h // 2, w - 12, 6))
    else:  # car
        pygame.draw.rect(surface, (30, 90, 220), (x, y, w, h))
        pygame.draw.rect(surface, (10, 20, 40), (x + 8, y + 8, w - 16, h // 3))
        pygame.draw.circle(surface, (10, 10, 10), (x + 14, y + h - 4), 8)
        pygame.draw.circle(surface, (10, 10, 10), (x + w - 14, y + h - 4), 8)


def draw_city_background(surface, w, h, offset=0):
    """Night city: gradient sky, moon, skyline, neon windows."""
    for yy in range(h):
        t = yy / max(1, h)
        col = (int(10 + 20 * t), int(10 + 30 * t), int(50 + 60 * t))
        pygame.draw.line(surface, col, (0, yy), (w, yy))
    pygame.draw.circle(surface, (230, 230, 200), (w - 90, 90), 42)
    pygame.draw.circle(surface, (200, 200, 180), (w - 90, 90), 34)
    import random
    rnd = random.Random(7)
    for i in range(14):
        bx = (i * 70 - offset % 70) % (w + 70) - 35
        bh = rnd.randint(90, 260)
        pygame.draw.rect(surface, (15, 15, 45), (bx, h - bh - 180, 60, bh + 180))
        for wy in range(0, bh, 26):
            for wx in range(6, 54, 16):
                if rnd.random() < 0.35:
                    pygame.draw.rect(surface, (255, 200, 80), (bx + wx, h - bh - 160 + wy, 8, 10))
