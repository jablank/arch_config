# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=2500
SAVEHIST=4000
unsetopt beep
bindkey -e
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/jab/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall

setopt append_history
setopt share_history
setopt hist_ignore_all_dups
setopt hist_reduce_blanks
setopt inc_append_history


# 2. Autosuggestions (must come AFTER compinit)
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh

export TZ="America/Phoenix"
export GTK_THEME=Adwaita:dark
export GTK2_RC_FILES=/usr/share/themes/Adwaita-dark/gtk-2.0/gtkrc
export QT_STYLE_OVERRIDE=Adwaita-Dark

# ---- Editor ----
export EDITOR="nano"
export VISUAL="nano"

# ---- WireGuard aliases ----
alias wgu='sudo wg-quick up lax'
alias wgd='sudo wg-quick down lax'
alias wgs='sudo wg show'

# ---- Brightness presets ----
alias sun0='ddcutil setvcp 10 0'
alias sun5='ddcutil setvcp 10 5'
alias sun10='ddcutil setvcp 10 10'
alias sun15='ddcutil setvcp 10 15'
alias sun20='ddcutil setvcp 10 20'
alias sun25='ddcutil setvcp 10 25'
alias sun30='ddcutil setvcp 10 30'
alias sun35='ddcutil setvcp 10 35'
alias sun40='ddcutil setvcp 10 40'
alias sun45='ddcutil setvcp 10 45'
alias sun50='ddcutil setvcp 10 50'
alias sun55='ddcutil setvcp 10 55'
alias sun60='ddcutil setvcp 10 60'
alias sun65='ddcutil setvcp 10 65'
alias sun70='ddcutil setvcp 10 70'
alias sun75='ddcutil setvcp 10 75'
alias sun80='ddcutil setvcp 10 80'
alias sun85='ddcutil setvcp 10 85'
alias sun90='ddcutil setvcp 10 90'
alias sun95='ddcutil setvcp 10 95'
alias sun100='ddcutil setvcp 10 100'

eval "$(zoxide init zsh)"
eval "$(starship init zsh)"
