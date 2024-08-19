import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import folder_paths
import torch
import svgwrite

class ComfyUISaveAs:
    ICO_SIZES = {
        "Small (32, 48, 64)": "32,48,64",
        "Medium (64, 128, 256)": "64,128,256",
        "Large (128, 256, 512)": "128,256,512"
    }

    RASTER_FORMATS = ["PNG", "JPG", "WEBP", "ICO", "GIF", "BMP", "TIFF"]
    VECTOR_FORMATS = ["SVG", "AI", "SVGZ", "DRW"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "image"}),
                "file_type": (["Raster", "Vector"],),
                "raster_format": (s.RASTER_FORMATS,),
                "vector_format": (s.VECTOR_FORMATS,),
                "quality": ([100, 95, 90, 85, 80, 75, 70, 60, 50], {"default": 100}),
            },
            "optional": {
                "ico_size_preset": (list(s.ICO_SIZES.keys()), {"default": "Large (128, 256, 512)"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    FUNCTION = "save_image"
    OUTPUT_NODE = True
    CATEGORY = "image/io"

    def save_image(self, images, filename_prefix, file_type, raster_format, vector_format, quality, ico_size_preset=None):
        save_dir = folder_paths.get_output_directory()
        format = raster_format.lower() if file_type == "Raster" else vector_format.lower()
        
        ico_sizes = None
        if format == "ico" and ico_size_preset:
            ico_sizes = [int(size) for size in self.ICO_SIZES[ico_size_preset].split(",")]
        
        saved_filenames = []

        for i, image in enumerate(images):
            img = Image.fromarray((255. * image.cpu().numpy()).astype(np.uint8))
            
            filename = self._generate_filename(save_dir, filename_prefix, i, format)
            
            try:
                if file_type == "Raster":
                    self._save_raster(img, filename, format, quality, ico_sizes)
                else:
                    self._save_vector(img, filename, format)
                
                print(f"Saved image as {filename}")
                saved_filenames.append(os.path.basename(filename))
            except Exception as e:
                print(f"Error saving {filename}: {str(e)}")

        # Create a preview image
        preview_image = self._create_preview(img, format, os.path.basename(filename))

        return (preview_image, ", ".join(saved_filenames))

    def _save_raster(self, img, filename, format, quality, ico_sizes):
        if format == "ico":
            if ico_sizes:
                self._save_ico(img, filename, ico_sizes)
            else:
                raise ValueError("ICO size preset is required for saving ICO files.")
        elif format in ["jpg", "jpeg"]:
            img.convert("RGB").save(filename, format="JPEG", quality=quality, subsampling=0)
        elif format == "webp":
            img.save(filename, format="WEBP", quality=quality, method=6)
        elif format == "gif":
            img.save(filename, format="GIF", optimize=True)
        elif format == "bmp":
            img.save(filename, format="BMP")
        elif format == "tiff":
            img.save(filename, format="TIFF", compression="tiff_lzw")
        else:  # png
            img.save(filename, format="PNG", optimize=True)

    def _save_vector(self, img, filename, format):
        if format == "svg":
            self._save_svg(img, filename)
        elif format == "ai":
            self._save_ai(img, filename)
        elif format == "svgz":
            self._save_svgz(img, filename)
        elif format == "drw":
            self._save_drw(img, filename)

    def _save_ico(self, img, filename, sizes):
        ico_images = []
        for size in sizes:
            resized_img = img.copy()
            resized_img.thumbnail((size, size), Image.LANCZOS)
            ico_images.append(resized_img)
        
        ico_images[0].save(filename, format="ICO", sizes=[(size, size) for size in sizes], quality=100)

    # ... (rest of the methods remain the same)

NODE_CLASS_MAPPINGS = {
    "ComfyUISaveAs": ComfyUISaveAs
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUISaveAs": "Save As"
}
