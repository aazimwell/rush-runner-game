#!/usr/bin/env python3
"""Render the programmatic sprites to PNG files + simple WAV effects.

Run: python3 generate_assets.py  (needs pygame-ce, desktop only)
Outputs are original drawings — no third-party images are copied.
"""
import math
import os
import struct
import wave

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame

from assets import CHARACTER_ORDER, draw_character, draw_city_background, draw_coin

ROOT = os.path.dirname(os.path.abspath(__file__))


def save_png(surface, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pygame.image.save(surface, path)
    print("wrote", path)


def tone(path, freq=440, ms=200, volume=0.3):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rate = 22050
    n = int(rate * ms / 1000)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        for i in range(n):
            v = int(volume * 32767 * math.sin(2 * math.pi * freq * i / rate))
            wf.writeframes(struct.pack("<h", v))
    print("wrote", path)


def main():
    pygame.init()
    for key in CHARACTER_ORDER:
        s = pygame.Surface((120, 160), pygame.SRCALPHA)
        draw_character(s, key, 60, 80, scale=1.3)
        save_png(s, os.path.join(ROOT, "assets", "characters", f"{key}.png"))
    bg = pygame.Surface((480, 720))
    draw_city_background(bg, 480, 720)
    save_png(bg, os.path.join(ROOT, "assets", "backgrounds", "city.png"))
    coin = pygame.Surface((48, 48), pygame.SRCALPHA)
    draw_coin(coin, 24, 24, 20)
    save_png(coin, os.path.join(ROOT, "assets", "images", "coin.png"))
    icon = pygame.Surface((512, 512))
    icon.fill((10, 10, 40))
    draw_city_background(icon, 512, 512)
    draw_character(icon, "robo", 256, 300, scale=2.2)
    save_png(icon, os.path.join(ROOT, "assets", "images", "icon.png"))
    save_png(icon, os.path.join(ROOT, "assets", "images", "presplash.png"))
    tone(os.path.join(ROOT, "assets", "sounds", "coin.wav"), 880, 150)
    tone(os.path.join(ROOT, "assets", "sounds", "jump.wav"), 520, 180)
    tone(os.path.join(ROOT, "assets", "sounds", "crash.wav"), 120, 300, volume=0.5)
    tone(os.path.join(ROOT, "assets", "sounds", "click.wav"), 660, 80)
    tone(os.path.join(ROOT, "assets", "sounds", "level_complete.wav"), 740, 400)
    print("done")


if __name__ == "__main__":
    main()
