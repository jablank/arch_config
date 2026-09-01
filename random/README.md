### Arch core
```bash


ly
> systemctl enable ly@tty2.service
> systemctl disable getty@tty2.service
# enable animations in /etc/ly/config.ini

ddcutil
> modprobe i2c-dev


```
##### pkgs
```bash

# shell utils
    emptty git flatpak jq bc \
    zsh zsh-autosuggestions zoxide tuned  
     
# security
    ufw openresolv wireguard-tools \
    hyprpolkitagent gnome-keyring
     
# devices
    pipewire pipewire-pulse i2c-tools 
    
# desktop
     mako swaybg hyprlock hypridle \
     slurp grim wl-clipboard wl-clip-persist cliphist \
     swayosd waybar rofi
    
# theme and fonts
    xdg-desktop-portal-gtk xdg-desktop-portal-hyprland starship \
    adwaita-qt6 adwaita-qt5 gnome-themes-extra \
    ttf-ubuntu-nerd ttf-ubuntu-mono-nerd noto-fonts-emoji

```



### Eye Mask Script - Requirements
```bash
python-opencv python-numpy
```
### zsh stuff 
[zoxide](https://github.com/ajeetdsouza/zoxide), [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md#packages), [starship](https://github.com/starship/starship)
