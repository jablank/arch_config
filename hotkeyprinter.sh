#!/usr/bin/env bash

# Query Hyprland for all binds with descriptions in JSON format
KEYBINDS_JSON=$(hyprctl binds -j)

# Use jq to parse the JSON and format it for Rofi
# Filter only binds with a description, then format as: 
# <key> + <keyval> | <description> | <command>
KEYBINDS_LIST=$(echo "$KEYBINDS_JSON" | jq -r '
    .[] 
    | select(.desc != null and .desc != "") 
    | "\(.mod) + \(.key) | \(.desc) | \(.disp)"
')

# Pipe the list to rofi
# The output format is set up so rofi returns the whole line
CHOICE=$(echo "$KEYBINDS_LIST" | rofi -dmenu -i -markup-rows -p "Hyprland Keybinds:")

# Exit if selection is empty (user closed rofi)
[[ -z "$CHOICE" ]] && exit

# Extract the command (the third field, delimited by '|')
CMD=$(echo "$CHOICE" | awk -F '|' '{print $3}' | xargs)

# Execute the command
if [[ $CMD == exec* ]]; then
    # Use eval for 'exec' commands
    eval "$CMD"
else
    # Use hyprctl dispatch for all other commands
    hyprctl dispatch "$CMD"
fi
