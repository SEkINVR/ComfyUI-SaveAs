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

    RETURN_TYPES = ()
    FUNCTION = "save_image"

    OUTPUT_NODE = True

    CATEGORY = "image"

    def save_image(self, images, filename_prefix, format, quality, ico_sizes):
        results = []
        
        # Ensure output directory exists
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            ico_sizes = [int(size.strip()) for size in ico_sizes.split(",")]
        except ValueError:
            print("Invalid ico_sizes format. Using default sizes.")
            ico_sizes = [16, 32, 48, 64, 128, 256]

        for i, image in enumerate(images):
            try:
                # Convert the image from tensor to PIL Image
                i = 255. * image.cpu().numpy()
                img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                
                # Generate filename
                file_extension = f".{format}"
                base_filename = f"{filename_prefix}_{i+1}"
                filename = os.path.join(output_dir, f"{base_filename}{file_extension}")
                counter = 1
                while os.path.exists(filename):
                    filename = os.path.join(output_dir, f"{base_filename}_{counter}{file_extension}")
                    counter += 1

                if format == "ico":
                    # For .ico, we need to create multiple sizes
                    ico_images = []
                    for size in ico_sizes:
                        ico_images.append(img.copy().resize((size, size), Image.LANCZOS))
                    ico_images[0].save(filename, format=format, sizes=[(size, size) for size in ico_sizes])
                elif format == "jpg":
                    # JPEG doesn't support alpha channel, so convert to RGB
                    img = img.convert("RGB")
                    img.save(filename, format=format, quality=quality)
                else:
                    img.save(filename, format=format, quality=quality)
                
                results.append({
                    "filename": filename,
                    "type": format
                })
                print(f"Saved image as {filename}")
            
            except Exception as e:
                print(f"Error saving image {i+1}: {str(e)}")
        
        return {"ui": {"images": results}}

NODE_CLASS_MAPPINGS = {
    "SaveMultiFormatImage": SaveMultiFormatImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveMultiFormatImage": "Save Multi-Format Image"
}
