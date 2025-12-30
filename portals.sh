#!/usr/bin/env bash
sleep 1
killall -e xdg-desktop-portal-hyprland
killall -e xdg-desktop-portal-wlr
killall xdg-desktop-portal
/usr/lib/xdg-desktop-portal-hyprland &
sleep 2
/usr/lib/xdg-desktop-portal &
# 1. Force the env variables into the session
exec-once = dbus-update-activation-environment --systemd --all

# 2. Use 'gentle' restarts for the portals
exec-once = systemctl --user restart xdg-desktop-portal-hyprland
exec-once = systemctl --user restart xdg-desktop-portal
