
## **defaults**
-  login | [emptty](https://github.com/tvrzna/emptty)
-  shell |  zsh + zoxide, autosuggest, starship
-  polkit |  keyring-gnome hyprpolkitagent 
-  power  |  ```tuned-adm profile latency-performance``` + hypridle hyprlock
-  network |  [ufw](https://wiki.archlinux.org/title/Uncomplicated_Firewall) openresolv
-  notifier | [mako](https://github.com/emersion/mako) [swayosd](https://github.com/ErikReider/SwayOSD)
-  status bars |  rofi, waybar 
-  screen |  ddcutil, i2c-tools, bash alias sunX x=0-100.
#### 
#### 
#### 
####

```bash
 # enable emptty, zsh newuser, ufw and tuned profile
emptty zsh zsh-autosuggestions zoxide tuned ufw \
hyprpolkitagent gnome-keyring \
openresolv wireguard-tools \
pipewire pipewire-pulse i2c-tools \
git flatpak \


# enable swaybg, hypridle, swayosd and waybar 
swaybg hyprlock hypridle slurp grim \
mako swayosd waybar rofi \
ttf-ubuntu-mono-nerd noto-fonts-emoji \

# theming
xdg-desktop-portal-gtk starship \
adwaita-qt6 adwaita-qt5 gnome-themes-extra \
 \

# for scripts
jq bc

```
autostart
```bash
exec-once = waybar &
exec-once = hypridle &
exec-once = swayosd-server & # uses ~100MB RAM
exec-once = systemctl --user start hyprpolkitagent
exec-once = /usr/bin/gnome-keyring-daemon --start --components=secrets &
exec-once = hyprctl setcursor Bibata-Modern-Ice 32
# makes sure hyprportal is prioritized
exec-once = killall -q xdg-desktop-portal-hyprland; killall -q xdg-desktop-portal; /usr/lib/xdg-desktop-portal-hyprland & /usr/lib/xdg-desktop-portal
```
env
```bash
env = XDG_CURRENT_DESKTOP,Hyprland
env = XDG_SESSION_TYPE,wayland
env = XDG_SESSION_DESKTOP,Hyprland
env = QT_QPA_PLATFORMTHEME=Adwaita-Dark
env = GTK_THEME=Adwaita:dark
env = GTK_APPLICATION_PREFER_DARK_THEME=1

env = HYPRCURSOR_THEME,Bibata-Modern-Ice
env = HYPRCURSOR_SIZE,32
# (X11 fallback)
env = XCURSOR_THEME,Bibata-Modern-Ice
env = XCURSOR_SIZE,32

```
### **low movement preset**
```bash
  decoration {
  rounding = 0
  active_opacity = 1.0
  inactive_opacity = 1.0
  blur { enabled = false }
  shadow { enabled = false }
  }
  ``` 


### to do
```bash
notifications
```
