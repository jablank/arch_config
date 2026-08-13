### outdated - hyprland is in lua now

autostart
```bash
exec-once = swaybg -i ~/Pictures/
exec-once = hyprctl setcursor Bibata-Modern-Ice 32
exec-once = waybar &

exec-once = hypridle &
exec-once = swayosd-server & # uses ~100MB RAM
exec-once = systemctl --user start hyprpolkitagent
exec-once = /usr/bin/gnome-keyring-daemon --start --components=secrets &
# makes sure hyprportal is prioritized
exec-once = killall -q xdg-desktop-portal-hyprland; killall -q xdg-desktop-portal; /usr/lib/xdg-desktop-portal-hyprland & /usr/lib/xdg-desktop-portal
```
env
```bash
env = MOZ_DISABLE_RDD_SANDBOX,1
env = LIBVA_DRIVER_NAME,nvidia
env = NVD_BACKEND,direct

env = XDG_CURRENT_DESKTOP,Hyprland
env = XDG_SESSION_TYPE,wayland
env = XDG_SESSION_DESKTOP,Hyprland

env = HYPRCURSOR_THEME,Bibata-Modern-Ice
env = HYPRCURSOR_SIZE,32
env = XCURSOR_THEME,Bibata-Modern-Ice
env = XCURSOR_SIZE,32
#https://wiki.archlinux.org/title/Dark_mode_switching
env = QT_QPA_PLATFORMTHEME=Adwaita-Dark
env = GTK_THEME=Adwaita:dark
env = GTK_APPLICATION_PREFER_DARK_THEME=1

```
### **hyprland low spec mode**
```bash
  decoration {
  rounding = 0
  active_opacity = 1.0
  inactive_opacity = 1.0
  blur { enabled = false }
  shadow { enabled = false }
  }
  ``` 
