"""Real accelerometer layer — never simulated with random values.

On Android, plyer.accelerometer is the real sensor source (Buildozer
recipes include plyer; add it to buildozer.spec if you enable tilt).
On desktop / devices without a sensor, ``available`` is False and the
game cleanly falls back to touch/keyboard only. Tilt on a real device
is UNVERIFIED until a device test — see README.
"""
try:
    from plyer import accelerometer as _accel
    _PLYER = True
except Exception:
    _accel = None
    _PLYER = False


class TiltSensor:
    def __init__(self):
        self.available = bool(_PLYER and _accel is not None)
        self.enabled = False
        self.offset_x = 0.0
        self._last_dir = 0  # -1 left, 0 neutral, 1 right (edge-triggered)

    def enable(self):
        if not self.available:
            return False
        try:
            _accel.enable()
            self.enabled = True
            return True
        except Exception:
            self.enabled = False
            return False

    def disable(self):
        if self.available and self.enabled:
            try:
                _accel.disable()
            except Exception:
                pass
        self.enabled = False

    def calibrate(self):
        """Store the current reading as neutral. Returns True if a sensor
        reading was available, else False (calibration is a no-op)."""
        val = self.read_raw()
        if val is None:
            return False
        self.offset_x = val[0]
        return True

    def read_raw(self):
        if not self.available or not self.enabled:
            return None
        try:
            v = _accel.acceleration
        except Exception:
            return None
        if v is None or len(v) < 1 or v[0] is None:
            return None
        return v

    def direction(self, sensitivity="Medium"):
        """Edge-triggered lane direction: -1 / 0 / +1.

        Dead-zone prevents jitter; a direction only fires once until the
        phone returns to neutral, so one tilt = one lane change.
        """
        if not self.available:
            return 0
        raw = self.read_raw()
        if raw is None:
            return 0
        dead = {"Low": 0.45, "Medium": 0.30, "High": 0.18}.get(sensitivity, 0.30)
        x = raw[0] - self.offset_x
        # On Android, tilting right typically gives negative x; invert so
        # tilt-right -> +1 (right lane). If your device reports the
        # opposite sign, flip it here — do not fake the value.
        direction = 0
        if x < -dead:
            direction = 1
        elif x > dead:
            direction = -1
        if direction != 0 and self._last_dir == direction:
            return 0  # already fired for this tilt; wait for neutral
        self._last_dir = direction
        return direction
