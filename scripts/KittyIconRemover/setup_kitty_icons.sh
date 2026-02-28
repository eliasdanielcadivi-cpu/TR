#!/bin/bash

# Configuration
SOURCE_IMAGE="/home/daniel/Descargas/ChatGPT Image 28 feb 2026, 11_56_33 a.m..png"
WORKSPACE_DIR="/home/daniel/Escritorio/KittyIconRemover"
BACKUP_DIR="$WORKSPACE_DIR/backups"
NEW_ICONS_DIR="$WORKSPACE_DIR/generated_icons"
PASS="a"

# Create necessary folders
mkdir -p "$BACKUP_DIR"
mkdir -p "$NEW_ICONS_DIR"

echo "Step 1: Copying source image to workspace..."
cp "$SOURCE_IMAGE" "$WORKSPACE_DIR/source_image.png"

# Function to handle PNG replacement
replace_png() {
    local target_path="$1"
    local filename=$(basename "$target_path")
    local dirname_hash=$(echo "$target_path" | md5sum | cut -d' ' -f1)
    local unique_name="${dirname_hash}_${filename}"
    
    echo "Processing PNG: $target_path"
    
    # Get target dimensions
    local dims=$(identify -format "%wx%h" "$target_path" 2>/dev/null || echo "256x256")
    
    # Generate new icon
    local new_icon_path="$NEW_ICONS_DIR/$unique_name"
    convert "$WORKSPACE_DIR/source_image.png" -resize "$dims" "$new_icon_path"
    
    # Backup original
    mkdir -p "$BACKUP_DIR/$(dirname "$target_path")"
    cp "$target_path" "$BACKUP_DIR/$target_path" 2>/dev/null
    
    # Replace (with sudo if needed)
    if [ -w "$target_path" ]; then
        cp "$new_icon_path" "$target_path"
    else
        echo "$PASS" | sudo -S cp "$new_icon_path" "$target_path"
    fi
}

# Function to handle SVG replacement (wrapping PNG in SVG)
replace_svg() {
    local target_path="$1"
    local filename=$(basename "$target_path")
    local dirname_hash=$(echo "$target_path" | md5sum | cut -d' ' -f1)
    local unique_name="${dirname_hash}_${filename}"
    
    echo "Processing SVG: $target_path"
    
    # Backup original
    mkdir -p "$BACKUP_DIR/$(dirname "$target_path")"
    cp "$target_path" "$BACKUP_DIR/$target_path" 2>/dev/null
    
    # We create a simple SVG that embeds the PNG base64
    local b64_png=$(base64 -w 0 "$WORKSPACE_DIR/source_image.png")
    local new_svg_path="$NEW_ICONS_DIR/$unique_name"
    
    cat <<EOF > "$new_svg_path"
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="512" height="512" viewBox="0 0 512 512">
  <image width="512" height="512" xlink:href="data:image/png;base64,$b64_png" />
</svg>
EOF

    # Replace (with sudo if needed)
    if [ -w "$target_path" ]; then
        cp "$new_svg_path" "$target_path"
    else
        echo "$PASS" | sudo -S cp "$new_svg_path" "$target_path"
    fi
}

# List of icons found earlier
ICON_LIST=(
"/home/daniel/.local/kitty.app/share/doc/kitty/html/_static/kitty.svg"
"/home/daniel/.local/kitty.app/share/icons/hicolor/scalable/apps/kitty.svg"
"/home/daniel/.local/kitty.app/share/icons/hicolor/256x256/apps/kitty.png"
"/home/daniel/.local/kitty.app/lib/kitty/logo/kitty.png"
"/home/daniel/.local/kitty.app/lib/kitty/logo/kitty-128.png"
"/usr/share/icons/Papirus/48x48/apps/kitty.svg"
"/usr/share/icons/Papirus/48x48/apps/appimagekit-kitty.svg"
"/usr/share/icons/Papirus/64x64/apps/kitty.svg"
"/usr/share/icons/Papirus/64x64/apps/appimagekit-kitty.svg"
"/usr/share/icons/Papirus/22x22/apps/kitty.svg"
"/usr/share/icons/Papirus/22x22/apps/appimagekit-kitty.svg"
"/usr/share/icons/Papirus/16x16/apps/kitty.svg"
"/usr/share/icons/Papirus/16x16/apps/appimagekit-kitty.svg"
"/usr/share/icons/Papirus/24x24/apps/kitty.svg"
"/usr/share/icons/Papirus/24x24/apps/appimagekit-kitty.svg"
"/usr/share/icons/Papirus/32x32/apps/kitty.svg"
"/usr/share/icons/Papirus/32x32/apps/appimagekit-kitty.svg"
)

for icon in "${ICON_LIST[@]}"; do
    if [[ "$icon" == *.png ]]; then
        replace_png "$icon"
    elif [[ "$icon" == *.svg ]]; then
        replace_svg "$icon"
    fi
done

echo "Refreshing icon cache..."
echo "$PASS" | sudo -S gtk-update-icon-cache /usr/share/icons/Papirus 2>/dev/null
echo "$PASS" | sudo -S gtk-update-icon-cache ~/.local/kitty.app/share/icons/hicolor 2>/dev/null

echo "Done! All icons substituted and backed up in $BACKUP_DIR"
