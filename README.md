
## **defaults**
-  login | emptty with default user
-  shell |  zsh with zoxide, autosuggest, starship
-  polkit |  keyring-gnome hyprpolkitagent 
-  power  |  ```tuned-adm profile latency-performance``` + hypridle hyprlock
-  firewall |  ufw and openresolv for dns
-  notifier | mako and swayosd for input popups
-  status bars |  rofi, waybar 
-  screen |  ddcutil, i2c-tools, bash alias sunX x=0-100.
#### 
#### 
#### 
####

```bash
# main, enable emptty, zsh newuser, ufw and tuned profile
emptty zsh zsh-autosuggestions zoxide tuned ufw \
hyprpolkitagent gnome-keyring \
openresolv wireguard-tools \
pipewire pipewire-pulse i2c-tools \
git flatpak \


# custom main
swaybg hyprlock hypridle slurp grim \
mako swayosd waybar rofi \
ttf-ubuntu-mono-nerd noto-fonts-emoji \

# theming
xdg-desktop-portal-gtk adwaita-qt5 adwaita-qt6 \
adwaita-qt6 adwaita-qt5 gnome-themes-extra \
starship \

# for scripts
jq bc

```
theme and env
```bash
exec-once = waybar &
exec-once = hypridle &
exec-once = swayosd-server & # uses ~100MB RAM
exec-once = systemctl --user start hyprpolkitagent
exec-once = /usr/bin/gnome-keyring-daemon --start --components=secrets &
exec-once = hyprctl setcursor Bibata-Modern-Ice 32
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
