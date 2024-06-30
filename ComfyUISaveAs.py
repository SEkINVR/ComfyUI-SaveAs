import os
from PIL import Image
import numpy as np
import folder_paths
import io
import base64
import cairosvg
import fitz  # PyMuPDF
from psd_tools import PSDImage
import rawpy
import moviepy.editor as mp

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
                "format": (["PNG", "JPG", "WEBP", "ICO", "GIF", "BMP", "TIFF", "MP4", "MOV", "SVG", "PDF", "PSD", "RAW"],),
                "quality": ([100, 95, 90, 85, 80, 75, 70, 60, 50],),
                "ico_size_preset": (list(s.ICO_SIZES.keys()),),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("preview_url",)
    FUNCTION = "save_media"
    OUTPUT_NODE = True
    CATEGORY = "image/io"
    
    def save_media(self, images, filename_prefix, format, quality, ico_size_preset):
        save_dir = folder_paths.get_output_directory()
        format = format.lower()
        
        ico_sizes = [int(size) for size in self.ICO_SIZES[ico_size_preset].split(",")]
        preview_urls = []
        
        for i, image in enumerate(images):
            img = Image.fromarray((255. * image.cpu().numpy()).astype(np.uint8))
            
            filename = self._generate_filename(save_dir, filename_prefix, i, format)
            
            try:
                if format in ["png", "jpg", "jpeg", "webp", "bmp", "tiff"]:
                    self._save_image(img, filename, format, quality)
                elif format == "ico":
                    self._save_ico(img, filename, ico_sizes)
                elif format == "gif":
                    img.save(filename, format="GIF")
                elif format in ["mp4", "mov"]:
                    self._save_video(img, filename, format)
                elif format == "svg":
                    self._save_svg(img, filename)
                elif format == "pdf":
                    self._save_pdf(img, filename)
                elif format == "psd":
                    self._save_psd(img, filename)
                elif format == "raw":
                    self._save_raw(img, filename)
                
                print(f"Saved media as {filename}")
                
                preview_url = self._generate_preview_url(img, format)
                preview_urls.append(preview_url)
                
            except Exception as e:
                print(f"Error saving {filename}: {str(e)}")
        
        return (", ".join(preview_urls),)
    
    def _save_image(self, img, filename, format, quality):
        if format in ["jpg", "jpeg"]:
            img.convert("RGB").save(filename, format="JPEG", quality=quality)
        elif format == "webp":
            img.save(filename, format="WEBP", quality=quality)
        else:
            img.save(filename, format=format.upper())
    
    def _save_video(self, img, filename, format):
        clip = mp.ImageClip(np.array(img)).set_duration(1)
        clip.write_videofile(filename, codec='libx264', fps=24)
    
    def _save_svg(self, img, filename):
        img.save(filename.replace('.svg', '.png'), format='PNG')
        cairosvg.svg2png(url=filename.replace('.svg', '.png'), write_to=filename)
        os.remove(filename.replace('.svg', '.png'))
    
    def _save_pdf(self, img, filename):
        img.save(filename, "PDF", resolution=100.0)
    
    def _save_psd(self, img, filename):
        psd = PSDImage.new(img.mode, img.size)
        psd.compose([img])
        psd.save(filename)
    
    def _save_raw(self, img, filename):
        with rawpy.imread(np.array(img)) as raw:
            raw.save(filename)
    
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
    
    def _generate_preview_url(self, img, format):
        buffer = io.BytesIO()
        
        if format in ["mp4", "mov"]:
            img.save(buffer, format="PNG")
        elif format in ["svg", "pdf", "psd", "raw"]:
            img.save(buffer, format="PNG")
        else:
            img.save(buffer, format=format.upper())
        
        encoded_media = base64.b64encode(buffer.getvalue()).decode()
        
        if format in ["mp4", "mov"]:
            return f"data:video/{format};base64,{encoded_media}"
        else:
            return f"data:image/{format};base64,{encoded_media}"

NODE_CLASS_MAPPINGS = {
    "ComfyUISaveAs": ComfyUISaveAs
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUISaveAs": "Save As"
}
