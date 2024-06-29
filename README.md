# ComfyUI Save Multi-Format Image Node

This custom node for ComfyUI allows you to save images in multiple formats, including PNG, JPG, WebP, and ICO.

## Features

- Save images in PNG, JPG, WebP, and ICO formats
- Customize quality for supported formats
- Specify multiple sizes for ICO files
- Automatically saves ICO files to `output/icon/icon.ico`

## Installation

1. Clone this repository into your ComfyUI's `custom_nodes` directory:
```bash
 git clone https://github.com/SEkINVR/ComfyUI-Save-Multi-Format.git
```
## Requirements

This custom node requires the following Python packages:
- Pillow >= 9.0.0
- numpy >= 1.20.0

These are usually already installed with ComfyUI, but if you encounter any issues, you can install them manually:
```bash
pip install -r requirements.txt
git add .gitignore requirements.txt
git commit -m "Add requirements.txt and .gitignore"
git push
