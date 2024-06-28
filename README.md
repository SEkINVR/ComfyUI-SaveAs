# sekinBatchAndSave-node
# Batch Image Save Node
Batch Image Save Node is a node designed to batch, process and save multiple images with specified extensions to a designated output directory. 
This README provides instructions on how to install and use the `BatchImageSaveNode` class in your Python project.

## Features

- **ImageBatch**: Manage batches of images for processing.
- **SaveImage**: Save images in formats such as PNG, JPEG, BMP, ICO, etc.
- **PreviewImage**: Preview images.
- **Example Node**: Illustrates integration with ComfyUI, processing images based on input parameters.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SEkINVR/sekinBatchAndSave-node.git
   cd sekinBatchAndSave-node
2. Install dependencies
   ```bash
   pip install -r requirements.txt
Usage
Example Node (Integration with ComfyUI)
Ensure your environment supports ComfyUI and Python dependencies.

Scripts and Classes
example.py: Contains examples of using ImageBatch, SaveImage, PreviewImage, and Example nodes.
ImageBatch.py, SaveImage.py, PreviewImage.py: Python classes for managing and processing images.
Compatibility
Tested with ComfyUI to ensure compatibility with its input/output formats and execution flow. Refer to ComfyUI documentation for specific integration guidelines.

Contributing
Fork the repository.
Create a branch (git checkout -b feature/your-feature).
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature/your-feature).
Create a new Pull Request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For issues, suggestions, or collaborations, please open an issue on GitHub 
