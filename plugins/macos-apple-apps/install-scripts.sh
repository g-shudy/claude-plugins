#!/bin/bash
# install-scripts.sh - Install helper scripts to ~/bin/

set -euo pipefail

PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$PLUGIN_DIR/scripts"
TARGET_DIR="$HOME/bin"

echo "macOS Apple Apps Plugin - Script Installer"
echo "==========================================="
echo ""

# Check if ~/bin exists
if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Creating $TARGET_DIR..."
    mkdir -p "$TARGET_DIR"
fi

# Check if ~/bin is in PATH
if [[ ":$PATH:" != *":$TARGET_DIR:"* ]]; then
    echo ""
    echo "⚠️  WARNING: $TARGET_DIR is not in your PATH"
    echo ""
    echo "Add this to your ~/.zshrc or ~/.bashrc:"
    echo "    export PATH=\"\$HOME/bin:\$PATH\""
    echo ""
    read -p "Continue anyway? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 1
    fi
fi

# List scripts to install
echo "Scripts to install:"
echo ""
for script in "$SCRIPTS_DIR"/*; do
    if [[ -f "$script" && -x "$script" ]]; then
        basename "$script"
    fi
done
echo ""

# Confirm installation
read -p "Install these scripts to $TARGET_DIR? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Installation cancelled."
    exit 0
fi

# Install scripts
echo ""
echo "Installing scripts..."
INSTALLED=0
SKIPPED=0

for script in "$SCRIPTS_DIR"/*; do
    if [[ -f "$script" && -x "$script" ]]; then
        script_name=$(basename "$script")
        target_path="$TARGET_DIR/$script_name"

        # Check if script already exists
        if [[ -f "$target_path" ]]; then
            echo "  ⚠️  $script_name (exists, skipping)"
            ((SKIPPED++))
        else
            cp "$script" "$target_path"
            chmod +x "$target_path"
            echo "  ✅ $script_name"
            ((INSTALLED++))
        fi
    fi
done

echo ""
echo "Installation complete!"
echo "  Installed: $INSTALLED scripts"
echo "  Skipped:   $SKIPPED scripts (already exist)"
echo ""

# Test installation
echo "Testing installation..."
if command -v calendar-list &> /dev/null; then
    echo "  ✅ Scripts are accessible in PATH"
else
    echo "  ⚠️  Scripts not found in PATH"
    echo "     You may need to restart your terminal or run:"
    echo "     source ~/.zshrc  (or ~/.bashrc)"
fi

echo ""
echo "Usage Examples:"
echo "  calendar-events --today"
echo "  contacts-search 'Marie'"
echo "  mail-unread"
echo "  imessage-recent -n"
echo "  imessage-search --felicitations"
echo "  reminders-list -o"
echo "  photos-query --last"
echo "  voice-memos list"
echo ""
echo "For help on any script, run: <script-name> --help"
