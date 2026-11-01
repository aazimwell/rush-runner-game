[app]
title = Rush Runner
package.name = rushrunner
package.domain = org.rush.runner
source.dir = .
source.include_exts = py,png,jpg,wav,json
version = 1.0.0
requirements = python3,pygame,plyer
orientation = portrait
fullscreen = 1
icon.filename = %(source.dir)s/assets/images/icon.png
presplash.filename = %(source.dir)s/assets/images/presplash.png
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a,armeabi-v7a
# Tilt sensor needs no extra permission on modern Android; keep the
# permission list minimal (offline game, no network).
android.permissions =
p4a.bootstrap = sdl2
p4a.local_recipes =
[buildozer]
log_level = 2
warn_on_root = 1
