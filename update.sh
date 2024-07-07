#!/bin/bash

# Find the ComfyUI installation directory
COMFYUI_DIR=$(dirname "$(dirname "$(readlink -f "$0")")")

# Define the path to the custom_nodes directory
CUSTOM_NODES_DIR="$COMFYUI_DIR/custom_nodes"

# Define the name of your node repository
NODE_REPO_NAME="ComfyUI-SaveAs"

# Check if the node directory exists
NODE_DIR="$CUSTOM_NODES_DIR/$NODE_REPO_NAME"
if [ ! -d "$NODE_DIR" ]; then
    echo "Error: $NODE_REPO_NAME directory not found in $CUSTOM_NODES_DIR"
    exit 1
fi

# Change to the node directory
cd "$NODE_DIR" || exit

# Fetch the latest changes
git fetch origin

# Check if there are any changes
if [ "$(git rev-parse HEAD)" != "$(git rev-parse @{u})" ]; then
    echo "Updates found. Updating the node..."
    
    # Pull the latest changes
    git pull origin main

    # Install or update requirements if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt --upgrade
    fi

    # Update the update script in the ComfyUI root directory
    cp update.sh "$COMFYUI_DIR/update_saveas.sh"
    chmod +x "$COMFYUI_DIR/update_saveas.sh"

    echo "ComfyUI SaveAs node has been updated successfully!"
else
    echo "ComfyUI SaveAs node is already up to date."
fi
