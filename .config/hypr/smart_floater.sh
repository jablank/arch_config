#!/bin/bash
# Script: /home/jab/.config/hypr/smart_floater.sh

# Exit if any command fails
set -e

# --- Configuration ---
# Factor to shrink the window size (0.8 = 80%)
RESIZE_FACTOR=0.90
# --- End Config ---

# Get JSON info for the active window
WINDOW_INFO=$(hyprctl activewindow -j)

# Use 'jq' to extract data
IS_FLOATING=$(echo "$WINDOW_INFO" | jq -r '.floating')
CURRENT_WIDTH=$(echo "$WINDOW_INFO" | jq -r '.size[0]')
CURRENT_HEIGHT=$(echo "$WINDOW_INFO" | jq -r '.size[1]')

if [ "$IS_FLOATING" = "true" ]; then
    # Already floating: Toggle back to tiled mode
    hyprctl dispatch togglefloating
else
    # Tiled: Calculate new size, then float, resize, and center
    # Use 'bc' for floating-point calculation
    NEW_WIDTH=$(echo "$CURRENT_WIDTH * $RESIZE_FACTOR" | bc | awk '{print int($1)}')
    NEW_HEIGHT=$(echo "$CURRENT_HEIGHT * $RESIZE_FACTOR" | bc | awk '{print int($1)}')

    # Batch dispatch for efficiency: toggle float, resize, then center
    hyprctl --batch "dispatch togglefloating; dispatch resizeactive exact $NEW_WIDTH $NEW_HEIGHT; dispatch centerwindow"
fi
