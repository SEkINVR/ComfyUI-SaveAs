# ComfyUI-SaveAs 

A custom node for ComfyUI that allows saving images and videos in multiple formats with a preview feature.

## Supported Formats

- Images: PNG, JPG, WEBP, ICO, GIF, BMP, TIFF
- Videos: MP4, MOV
- Others: SVG, PDF, PSD, RAW
- 
## Features
- Supports PNG, JPG, WEBP, ICO, GIF, BMP, and TIFF formats
- ICO size presets
- Preview of saved image and filenames
- Customize quality for supported formats

## Installation

1. Clone this repository into your ComfyUI's `custom_nodes` directory:
```bash
 git clone https://github.com/SEkINVR/ComfyUI-SaveAs.git
```
2. Install the required dependencies:
```bash
 pip install -r requirements.txt
```

## Requirements

This custom node requires the following Python packages:
- Pillow >= 9.0.0
- numpy >= 1.20.0

## Usage

1. In ComfyUI, you'll find a new node called "Save As" under the "image/io" category.
2. Connect an image output to this node.
3. Choose your desired format and settings.
4. Run the workflow to save your image and generate a preview.


These are usually already installed with ComfyUI, but if you encounter any issues, you can install them manually:
```bash
pip install -r requirements.txt
git add .gitignore requirements.txt
git commit -m "Add requirements.txt and .gitignore"
git push
```
Node>
```
ComfyUI-SaveAs/
│
├── __init__.py
├── ComfyUISaveAs.py
├── README.md
├── requirements.txt (if needed)
├── install.sh
├── update.sh
└── examples/ (optional)
    └── example_workflow.png
```
