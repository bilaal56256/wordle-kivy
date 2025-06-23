[app]
title = WordleKivy
package.name = wordlekivy
package.domain = org.bilaal.wordle
source.dir = .
source.include_exts = py,png,ttf,txt
version = 1.0
requirements = kivy, kivmob
orientation = portrait
fullscreen = 1

android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-1644069676777509~2139726918
android.gradle_dependencies = com.google.android.gms:play-services-ads:20.3.0

[buildozer]
log_level = 2
warn_on_root = 1