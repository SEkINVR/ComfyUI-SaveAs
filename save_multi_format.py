import os
from PIL import Image
import numpy as np
import folder_paths

class SaveMultiFormatImage:
    ICO_SIZES = {
        "small": "16,32,48",
        "medium": "16,32,48,64,128",
        "large": "16,32,48,64,128,256"
    }

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "image"}),
                "format": (["png", "jpg", "webp", "ico"],),
                "quality": ([1, 25, 50, 75, 95, 100],),
                "ico_size_preset": (list(s.ICO_SIZES.keys()),),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "filename")
    FUNCTION = "save_image"
    OUTPUT_NODE = True
    CATEGORY = "image"

    def save_image(self, images, filename_prefix, format, quality, ico_size_preset):
        save_dir = folder_paths.get_output_directory()
        
        ico_sizes = [int(size) for size in self.ICO_SIZES[ico_size_preset].split(",")]

        results = []
        for i, image in enumerate(images):
            img = Image.fromarray((255. * image.cpu().numpy()).astype(np.uint8))
            
            if format == "ico":
                filename = self._generate_filename(save_dir, "icon", i, format)
            else:
                filename = self._generate_filename(save_dir, filename_prefix, i, format)
            
            if format == "ico":
                self._save_ico(img, filename, ico_sizes)
            elif format == "jpg":
                img.convert("RGB").save(filename, format=format, quality=quality)
            elif format == "webp":
                img.save(filename, format=format, quality=quality)
            else:  # png
                img.save(filename, format=format)
            
            results.append({
                "filename": filename,
                "type": format
            })
            print(f"Saved image as {filename}")

        # Return the last saved image for preview
        return (images[-1], results[-1]["filename"])

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
        ico_images[0].save(filename, format="ico", sizes=[(size, size) for size in sizes])

NODE_CLASS_MAPPINGS = {
    "SaveMultiFormatImage": SaveMultiFormatImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveMultiFormatImage": "Save Multi-Format Image"
}
