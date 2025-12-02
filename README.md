
## **entry**

- **dm** | [emptty](https://github.com/tvrzna/emptty)
- **shell** | zsh + [zoxide](https://github.com/ajeetdsouza/zoxide), [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md#packages), [starship](https://github.com/starship/starship)
- **keys** | keyring-gnome, hyprpolkitagent
- **power** | [tuned](https://github.com/redhat-performance/tuned)  + hypridle, hyprlock
- **network** | [ufw](https://wiki.archlinux.org/title/Uncomplicated_Firewall), openresolv, wireguard-tools
- **screen** | grim, slurp, ddcutil, i2c-tools
- **fonts** | ubuntu nerd, adwaita sans


####

```bash
core++ >
## 
  sudo systemctl enable --now tuned ufw gnome-keyring-daemon
## tuned-adm list
  tuned-adm profile latency-performance

# shell utils
    zsh zsh-autosuggestions zoxide tuned \ 
    git flatpak jq bc 
    
# keys network
    ufw hyprpolkitagent gnome-keyring \
    openresolv wireguard-tools \
    
# devices
    pipewire pipewire-pulse i2c-tools 
    
# desktop environment
    emptty swaybg hyprlock hypridle slurp grim \
    mako swayosd waybar rofi 
    
# theme and fonts
    xdg-desktop-portal-gtk starship \
    adwaita-qt6 adwaita-qt5 gnome-themes-extra \
    ttf-ubuntu-nerd ttf-ubuntu-mono-nerd noto-fonts-emoji

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
### **hyprland low movement**
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
