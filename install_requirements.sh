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
    echo "Please make sure you have installed the ComfyUI-SaveAs node correctly."
    exit 1
fi

# Change to the node directory
cd "$NODE_DIR" || exit

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing requirements for ComfyUI SaveAs node..."
    pip install -r requirements.txt --upgrade
    echo "Requirements installed successfully!"
else
    echo "No requirements.txt found. No additional packages need to be installed."
fi

echo "ComfyUI SaveAs node requirements installation complete!"
