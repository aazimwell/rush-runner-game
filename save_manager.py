"""Local persistence for Rush Runner. JSON only, no network, no accounts.

File location (desktop): next to the game, ``save.json``.
On Android (Buildozer) the same relative path lives in the app's
private storage, so coins / high score survive restarts but never leave
the device.
"""
import json
import os

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save.json")

DEFAULTS = {
    "coins": 12560,          # starter balance, matching the reference HUD
    "diamonds": 250,
    "high_score": 0,
    "best_distance": 0,
    "selected_character": "robo",
    "settings": {
        "music": True,
        "sound": True,
        "graphics": "High",          # Low / Medium / High
        "control_style": "Touch",     # Touch (swipe) — see control_mode below
        "language": "English",
        "control_mode": "touch",      # touch / tilt / both
        "sensitivity": "Medium",      # Low / Medium / High
    },
}


def load():
    """Return a deep copy of the saved data, merged over DEFAULTS."""
    data = json.loads(json.dumps(DEFAULTS))
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as fh:
            saved = json.load(fh)
        if isinstance(saved, dict):
            data.update(saved)
            if isinstance(saved.get("settings"), dict):
                merged = dict(DEFAULTS["settings"])
                merged.update(saved["settings"])
                data["settings"] = merged
    except (OSError, ValueError):
        pass
    return data


def save(data):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        return True
    except OSError:
        return False
