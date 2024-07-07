import os
from PIL import Image
import numpy as np
import folder_paths
import torch

class ComfyUISaveAs:
    ICO_SIZES = {
        "Small (16, 32, 48)": "16,32,48",
        "Medium (16, 32, 48, 64, 128)": "16,32,48,64,128",
        "Large (16, 32, 48, 64, 128, 256)": "16,32,48,64,128,256"
    }

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "image"}),
                "format": (["PNG", "JPG", "WEBP", "ICO", "GIF", "BMP", "TIFF"],),
                "quality": ([100, 95, 90, 85, 80, 75, 70, 60, 50],),
                "ico_size_preset": (list(s.ICO_SIZES.keys()),),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    FUNCTION = "save_image"
    OUTPUT_NODE = True
    CATEGORY = "image/io"

    def save_image(self, images, filename_prefix, format, quality, ico_size_preset):
        save_dir = folder_paths.get_output_directory()
        format = format.lower()
        
        ico_sizes = [int(size) for size in self.ICO_SIZES[ico_size_preset].split(",")]
        saved_filenames = []

        for i, image in enumerate(images):
            img = Image.fromarray((255. * image.cpu().numpy()).astype(np.uint8))
            
            filename = self._generate_filename(save_dir, filename_prefix, i, format)
            
            try:
                if format == "ico":
                    self._save_ico(img, filename, ico_sizes)
                elif format in ["jpg", "jpeg"]:
                    img.convert("RGB").save(filename, format="JPEG", quality=quality)
                elif format in ["webp", "gif", "bmp", "tiff"]:
                    img.save(filename, format=format.upper(), quality=quality)
                else:  # png
                    img.save(filename, format="PNG")
                
                print(f"Saved image as {filename}")
                saved_filenames.append(os.path.basename(filename))
            except Exception as e:
                print(f"Error saving {filename}: {str(e)}")

        # Return the last saved image for preview
        return (images[-1:], ", ".join(saved_filenames))

    def _generate_filename(self, save_dir, prefix, index, format):
        base_filename = f"{prefix}_{index+1}.{format}"
        filename = os.path.join(save_dir, base_filename)
        counter = 1
        while os.path.exists(filename):
            filename = os.path.join(save_dir, f"{prefix}_{index+1}_{counter}.{format}")
            counter += 1
        return filename

    def _save_ico(self, img, filename, sizes):
        ico_images = [img.copy().resize((size, size), Image.LANCZOS) for size in sizes]
        ico_images[0].save(filename, format="ICO", sizes=[(size, size) for size in sizes])

NODE_CLASS_MAPPINGS = {
    "ComfyUISaveAs": ComfyUISaveAs
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUISaveAs": "Save As"
}
