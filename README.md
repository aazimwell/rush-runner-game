# Rush Runner — Endless Adventure

A complete, playable, offline endless-runner game in Python (Pygame API),
in portrait mode, with a neon night-city look inspired by the reference
image (original art only — the reference image itself is NOT copied).

## Compatibility gate — read this first (honest, not hidden)

**Desktop Pygame does NOT automatically become an Android APK.**
The Android route in this project is:

- **Buildozer + python-for-android, SDL2 bootstrap**
- Requirements: `python3, pygame-ce` (pygame-ce is the maintained
  Pygame-API fork; the recipe pattern for it is a known community
  gist pattern, not a stock Pygame recipe)
- **PGS4A is old / Python 2 and is NOT used here.**

**APK success is only proven when the GitHub Actions run succeeds.**
There is no APK download link in this README, and none is claimed.
If the Actions build fails, its log — not a claim — is the truth.

**Accelerometer on a real device: UNVERIFIED.**
Tilt uses `plyer.accelerometer` when present on Android, with a clean
fallback to touch-only when the sensor is unavailable. It is never
simulated with random values. Touch/swipe always works, so the game
is fully playable without tilt.

## What is in the game

- Main menu: PLAY, CHARACTER, SETTINGS, HIGH SCORE, QUIT — all functional
- Character select: Robo Runner, Female Runner, Shadow Runner, Panda Runner
  (PREV / NEXT / SELECT / BACK; selection actually changes the sprite)
- Gameplay: 3 lanes, jump, slide, coins, obstacles, collision,
  score / distance / speed that increases, pause
- Pause: RESUME / RESTART / SETTINGS / HOME
- Level complete every 1000 m (trophy, score, coins, distance, 3 stars,
  HOME / NEXT) and Game over (score, best, coins, RESTART / HOME)
- Settings: music, sound, graphics quality, control style, language,
  control mode (Touch / Tilt / Both), sensitivity (Low / Medium / High),
  tilt calibration — all persisted locally in `save.json`
- Controls: swipe left / right / up / down (dead-zone, one action per
  touch), keyboard arrows / space on desktop, tilt via sensors.py
- Offline: no login, no accounts, no server, no ads, no downloads.
  All assets are bundled; the game works in airplane mode.

## Project structure

```
main.py               # entry point + state machine
game.py               # gameplay, road, HUD, collisions, milestones
menu.py               # menu / character / settings / pause / results
player.py             # 3-lane player, jump, slide
obstacles.py          # obstacles + coins, pseudo-3D depth
coins.py              # coin value / score
controls.py           # swipe detector + keyboard map
sensors.py            # plyer accelerometer, calibrated, edge-triggered
settings.py           # settings wrapper over save_manager
save_manager.py       # JSON persistence (coins, high score, settings)
assets.py             # original programmatic sprites
ui_components.py      # solid-colour buttons / panels (no gradient buttons)
generate_assets.py    # renders PNGs + WAVs from assets.py
assets/images/ assets/characters/ assets/backgrounds/
assets/icons/ assets/sounds/ assets/fonts/   # fonts: system/default fallback
buildozer.spec        # Android packaging config
.github/workflows/android-apk.yml
```

## Run on desktop

```bash
pip install pygame-ce
python3 main.py
# optional: render bundled PNG/WAV assets first
python3 generate_assets.py
```

Controls on desktop: ← → lanes, ↑ / Space jump, ↓ slide, P pause, Esc back.

## Build the APK from an Android phone only (GitHub)

1. Create a GitHub repository named **rush-runner-game** (public or private).
2. Upload this whole project using GitHub's website on Android:
   use *Add file → Upload files* (upload in batches if needed), keeping
   the folder structure, especially `.github/workflows/android-apk.yml`.
   Note: GitHub's web uploader can hide dot-folders — if `.github` does
   not appear after upload, create it via *Add file → Create new file*
   with the path `.github/workflows/android-apk.yml` and paste the
   workflow file content.
3. Open the **Actions** tab in the repository.
4. Run the workflow **Build Android APK** (it also runs on push to main).
5. Watch the run; if it fails, open the failed step and read its log.
6. On a successful run, download the artifact named
   **RUSH-RUNNER-ANDROID-APK** and install the APK on your phone
   (allow "install unknown apps" for your browser/file manager once).
7. Test in airplane mode: menu → Play → swipe, coins, pause, game over,
   settings persistence, high score persistence.

## Testing checklist

- [ ] Home screen opens, all five menu buttons work
- [ ] Play starts a real game; lanes, jump, slide work
- [ ] Swipe left/right/up/down work (desktop: arrow keys)
- [ ] Coins can be collected; obstacles end a run on collision
- [ ] Score increases with distance and coins
- [ ] Pause / resume / restart work; game over works
- [ ] Level complete appears at 1000 m; NEXT continues
- [ ] High score and coins persist after restart
- [ ] Settings persist after restart
- [ ] Offline mode works (airplane mode)
- [ ] Android back navigation handled (Esc / menu back)
- [ ] Tilt on a real device — UNVERIFIED until device test
- [ ] GitHub Actions APK build — UNVERIFIED until the run succeeds

## Troubleshooting

- **Actions build fails on Cython:** the workflow pins `Cython<3.0`;
  do not upgrade it without checking python-for-android compatibility.
- **No tilt on a device:** the game falls back to touch-only and the
  Settings screen shows "TILT: NO SENSOR". This is expected on
  devices without plyer/sensor support — it is not a crash.
- **APK installs but shows a black screen:** check the Actions log
  for missing assets, and that `assets/` was uploaded intact.
- **Buttons do nothing:** every button in menu.py is checked in
  main.py; if a screen is blank, run `python3 main.py` on desktop
  first and read the traceback.
