import os

class BatchImageSaveNode:
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    CATEGORY = "Image Processing"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "extension": ([".png", ".ico", ".jpeg", ".gif"],),
            }
        }

    def execute(self, images, save_path=None, extension=".png"):
        # Set default save path
        default_save_path = os.path.join("C:", "ComfyUI_windows_portable", "ComfyUI", "output")
        
        # Check if the default path exists and is writable
        if not os.path.exists(default_save_path):
            os.makedirs(default_save_path, exist_ok=True)  # Create directory if it doesn't exist
        
        saved_files = []
        for i, image in enumerate(images):
            filename = f"image_{i}.{extension.strip('.')}"
            full_path = os.path.join(default_save_path, filename)
            # Example save operation
            image.save(full_path)  # Replace with actual saving logic
            saved_files.append(full_path)
        return (saved_files,)
