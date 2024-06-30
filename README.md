# ComfyUI SaveAS

This custom node for ComfyUI allows you to save images in multiple formats, including PNG, JPG, WebP, and ICO.

## Features

- Save images in PNG, JPG, WebP, and ICO formats
- Customize quality for supported formats
- Specify multiple sizes for ICO files

 ## To use this node:
1. Connect your image output to this node.
2. Set the filename_prefix as desired.
3. Choose the format you want (png, jpg, webp, or ico).
4. Set the quality for formats that support it.
5. For ico format, specify the sizes in ico_sizes.
6. Optionally, specify an output_dir if you want to save in a specific location.

## Installation

1. Clone this repository into your ComfyUI's `custom_nodes` directory:
```bash
 git clone https://github.com/SEkINVR/ComfyUI-SaveAs.git
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
