import os
from PIL import Image
import numpy as np

class SaveMultiFormatImage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "image"}),
                "format": (["png", "jpg", "webp", "ico"],),
                "quality": ("INT", {"default": 95, "min": 1, "max": 100, "step": 1}),
                "ico_sizes": ("STRING", {"default": "16,32,48,64,128,256"}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "save_image"
    OUTPUT_NODE = True
    CATEGORY = "image"

    def save_image(self, images, filename_prefix, format, quality, ico_sizes):
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        ico_sizes = [int(size.strip()) for size in ico_sizes.split(",")]

        for i, image in enumerate(images):
            img = Image.fromarray((255. * image.cpu().numpy()).astype(np.uint8))
            
            filename = self._generate_filename(output_dir, filename_prefix, i, format)

            if format == "ico":
                self._save_ico(img, filename, ico_sizes)
            elif format == "jpg":
                img.convert("RGB").save(filename, format=format, quality=quality)
            else:
                img.save(filename, format=format, quality=quality)
            
            print(f"Saved image as {filename}")

        return (images,)

    def _generate_filename(self, output_dir, prefix, index, format):
        base_filename = f"{prefix}_{index+1}.{format}"
        filename = os.path.join(output_dir, base_filename)
        counter = 1
        while os.path.exists(filename):
            filename = os.path.join(output_dir, f"{prefix}_{index+1}_{counter}.{format}")
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
