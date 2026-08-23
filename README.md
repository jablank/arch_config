# 
### to do
```bash
egr
```
### current
2026 08 10 fedora/gnome

2026 07 27 [labwc](https://github.com/jablank/xfceland) waiting for xfwl4 

2026 06 04 gnome

2025 12 21 [noctalia](https://github.com/noctalia-dev)


## **arch entry**

- **dm** | [ly](https://github.com/fairyglade/ly)
- **shell** | bash + [blesh](https://github.com/akinomyoga/ble.sh) + starship
- **keys** | keyring-gnome, hyprpolkitagent
- **power** | [tuned](https://github.com/redhat-performance/tuned), hypridle, hyprlock
- **network** | [ufw](https://wiki.archlinux.org/title/Uncomplicated_Firewall), openresolv, wireguard-tools
- **hw** | grim, slurp, ddcutil, i2c-tools
- **text** | ubuntu nerd, adwaita sans, cliphist

#### GMKTec G3 Plus dummy plug disable for display manager

in /etc/default/grub

``` GRUB_CMDLINE_LINUX="... quiet splash video=HDMI-A-2:d" ``` 

#### Hardware Decoding on Nvidia + Chromium
```
1. cp /usr/share/applications/brave-origin-nightly.desktop ~/.local/share/applications/
2. Exec=/usr/bin/brave-origin-nightly --enable-features=AcceleratedVideoDecodeLinuxGL,AcceleratedVideoDecodeLinuxZeroCopyGL,VaapiIgnoreDriverChecks,VaapiOnNvidiaGPUs --ozone-platform=wayland %U

```


##### core
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

