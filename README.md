
## Current
2026 08 10 fedora/gnome

2026 07 27 [labwc](https://github.com/jablank/xfceland) waiting for xfwl4 

2026 06 04 gnome

2025 12 21 [noctalia](https://github.com/noctalia-dev)


## GMKTec G3 Plus ACPI fix
#### Issue
Phantom display stealing GDM primary output and loss of video signal on wake from sleep.

#### Solution
Updated `/etc/default/grub` with kernel parameters:
```GRUB_CMDLINE_LINUX="rhgb quiet video=HDMI-A-2:d video=HDMI-A-1:e i915.enable_dc=0 mem_sleep_default=s2idle"```


## Hardware Decoding on Nvidia + Chromium
```
1. cp /usr/share/applications/brave-origin-nightly.desktop ~/.local/share/applications/
2. Exec=/usr/bin/brave-origin-nightly --enable-features=AcceleratedVideoDecodeLinuxGL,AcceleratedVideoDecodeLinuxZeroCopyGL,VaapiIgnoreDriverChecks,VaapiOnNvidiaGPUs --ozone-platform=wayland %U

```

## **arch entry**

- **dm** | [ly](https://github.com/fairyglade/ly)
- **shell** | bash + [blesh](https://github.com/akinomyoga/ble.sh) + [starship](https://github.com/starship/starship)
- **keys** | keyring-gnome, hyprpolkitagent
- **power** | [tuned](https://github.com/redhat-performance/tuned), hypridle, hyprlock
- **network** | [ufw](https://wiki.archlinux.org/title/Uncomplicated_Firewall), openresolv, wireguard-tools
- **hw** | grim, slurp, ddcutil, i2c-tools
- **text** | ubuntu nerd, adwaita sans, cliphist







