
## **arch entry**

- **dm** | [emptty](https://github.com/tvrzna/emptty)
- **shell** | zsh + [zoxide](https://github.com/ajeetdsouza/zoxide), [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md#packages), [starship](https://github.com/starship/starship)
- **security** | keyring-gnome, hyprpolkitagent, keepassxc
- **power** | [tuned](https://github.com/redhat-performance/tuned), hypridle, hyprlock
- **network** | [ufw firewall](https://wiki.archlinux.org/title/Uncomplicated_Firewall), openresolv, wireguard-tools
- **hardware** | grim, slurp, ddcutil, i2c-tools
- **text** | ubuntu nerd, adwaita sans, cliphist


####

```bash
core++ >

1. sudo systemctl enable --now tuned ufw gnome-keyring-daemon
2. tuned-adm profile latency-performance
3. modprobe i2c-dev
  
yay -S --repo 

# shell utils
    emptty git flatpak jq bc \
    zsh zsh-autosuggestions zoxide tuned  
     
# security
    ufw openresolv wireguard-tools \
    hyprpolkitagent gnome-keyring keepassxc
     
# devices
    pipewire pipewire-pulse i2c-tools 
    
# desktop environment
     mako swaybg hyprlock hypridle \
     slurp grim wl-clipboard wl-clip-persist cliphist \
     swayosd waybar rofi
     
    
# theme and fonts
    xdg-desktop-portal-gtk starship \
    adwaita-qt6 adwaita-qt5 gnome-themes-extra \
    ttf-ubuntu-nerd ttf-ubuntu-mono-nerd noto-fonts-emoji

```
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
