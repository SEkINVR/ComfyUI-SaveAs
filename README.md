# ComfyUI-SaveAs 
A custom node for ComfyUI that allows saving images in multiple formats with advanced options and a preview feature.

## Supported Formats
- Images: PNG, JPG, WEBP, ICO, GIF, BMP, TIFF

## Features
- High-quality saving for all supported formats
- Customizable quality settings for applicable formats
- ICO size presets (Small, Medium, Large)
- Preview of saved image and filenames
- Automatic file naming to prevent overwrites

## Installation
1. Clone this repository into your ComfyUI's `custom_nodes` directory:
   ```bash
   git clone https://github.com/SEkINVR/ComfyUI-SaveAs.git
   ```
2. Navigate to the ComfyUI-SaveAs directory:
   ```bash
   cd ComfyUI-SaveAs
   ```
3. Run the installation script:
   ```bash
   ./install_requirements.sh
   ```

## Requirements
This custom node requires the following Python package:
- Pillow >= 9.5.0

This is usually already installed with ComfyUI, but the installation script will ensure you have the correct version.

## Usage
1. In ComfyUI, you'll find a new node called "Save As" under the "image/io" category.
2. Connect an image output to this node.
3. Choose your desired format, quality, and ICO size preset (if applicable).
4. Run the workflow to save your image and generate a preview.

## Updating
To update the node to the latest version:

1. Navigate to your ComfyUI root directory.
2. Run the following command:
   ```bash
   ./custom_nodes/ComfyUI-SaveAs/update.sh
   ```

## Repository Structure
```
ComfyUI-SaveAs/
│
├── __init__.py
├── ComfyUISaveAs.py
├── README.md
├── requirements.txt
├── install_requirements.sh
├── update.sh
└── examples/
    └── PC_Icon_creator_Workflow.json
    └── PC_Icon_creator_Workflow.png
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
[MIT License](https://opensource.org/licenses/MIT)
```

This updated README reflects the current state of your project, including:

1. The accurate list of supported image formats.
2. Updated features, including high-quality saving and preview capabilities.
3. Correct installation instructions using the `install_requirements.sh` script.
4. Updated requirements, specifying Pillow >= 9.5.0.
5. Instructions for updating the node using the `update.sh` script.
6. An accurate repository structure.
