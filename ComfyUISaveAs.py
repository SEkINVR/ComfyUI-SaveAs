import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import folder_paths
import torch

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
        try:
            import svgwrite
        except ImportError:
            raise ImportError("The 'svgwrite' module is required for saving vector graphics. Please install it using 'pip install svgwrite'.")

        if format == "svg":
            self._save_svg(img, filename)
        elif format == "ai":
            self._save_ai(img, filename)
        elif format == "svgz":
            self._save_svgz(img, filename)
        elif format == "drw":
            self._save_drw(img, filename)

    def _save_svg(self, img, filename):
        dwg = svgwrite.Drawing(filename, size=img.size)
        dwg.add(dwg.image(href=self._image_to_data_uri(img), size=img.size))
        dwg.save()

    def _save_ai(self, img, filename):
        # For simplicity, we'll save as SVG and rename to .ai
        svg_filename = filename[:-3] + ".svg"
        self._save_svg(img, svg_filename)
        os.rename(svg_filename, filename)

    def _save_svgz(self, img, filename):
        import gzip
        svg_content = self._get_svg_content(img)
        with gzip.open(filename, 'wb') as f:
            f.write(svg_content.encode('utf-8'))

    def _save_drw(self, img, filename):
        # For simplicity, we'll save as SVG and rename to .drw
        svg_filename = filename[:-4] + ".svg"
        self._save_svg(img, svg_filename)
        os.rename(svg_filename, filename)

    def _get_svg_content(self, img):
        dwg = svgwrite.Drawing(size=img.size)
        dwg.add(dwg.image(href=self._image_to_data_uri(img), size=img.size))
        return dwg.tostring()

    def _image_to_data_uri(self, img):
        import base64
        from io import BytesIO
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()

    # ... (rest of the methods remain the same)

NODE_CLASS_MAPPINGS = {
    "ComfyUISaveAs": ComfyUISaveAs
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUISaveAs": "Save As"
}
