[app]
title = WordleKivy
package.name = wordlekivy
package.domain = org.bilaal.wordle
source.dir = .
source.include_exts = py,png,ttf,txt
version = 1.0
requirements = python3,kivy==2.2.1,kivmob==1.3.2
orientation = portrait
fullscreen = 1
osx.python_version = 3

# Android configuration #hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
android.api = 31
android.minapi = 21
android.sdk = 30
android.ndk = 23b
android.build_tools_version = 30.0.3
android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-1644069676777509~2139726918
android.gradle_dependencies = com.google.android.gms:play-services-ads:20.3.0
android.enable_androidx = 1
android.use_android_native_api = False
android.archs = arm64-v8a,armeabi-v7a

# Optional image and font assets
presplash.filename = splash.png
icon.filename = icon.png

[buildozer]
log_level = 2
warn_on_root = 1
