import json
import os
from nodes import EmptyLatentImage

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the config file
config_path = os.path.join(script_dir, 'Latent_Image_Size_config.json')

with open(config_path, 'r') as file:
    config = json.load(file)

class ComfyUI_EXO_LatentImageSize:
    NAME = "ComfyUI_EXO_Latent Image Size 👑"
    CATEGORY = "Custom EXO Nodes"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "dimensions": (
                    config["dimensions"],
                    {
                        "default": config["default"],
                        "tooltip": "Select the desired dimensions for your latent image. Format: width x height (aspect ratio)"
                    }),
                "batch_size": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 64,
                    "tooltip": "Number of images to generate in a single batch. Higher values use more VRAM."
                }),
            },
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("Latent",)
    OUTPUT_TOOLTIPS = ("The latent image noise at the specified dimensions. Connect to nodes that process latent images.",)
    FUNCTION = "generate"

    def generate(self, dimensions, batch_size):
        """
        Generates an empty latent image at the specified dimensions and batch size.
        
        Args:
            dimensions (str): The dimensions string in format 'width x height (aspect ratio)'
            batch_size (int): Number of images to generate in batch
        
        Returns:
            tuple: Contains the generated latent image
        """
        # Check if the selected item is a separator or space
        if dimensions.startswith('-----') or dimensions.strip() == "":
            raise ValueError("Please select a valid dimension setting, not a separator line")
            
        # Extract dimensions from the string (ignore the aspect ratio label in parentheses)
        dimensions_part = dimensions.split('(')[0].strip()
        result = [x.strip() for x in dimensions_part.split('x')]
        width = int(result[0])
        height = int(result[1])
        latent = EmptyLatentImage().generate(width, height, batch_size)[0]
        return (latent,)

# Register node mappings
NODE_CLASS_MAPPINGS = {
    "ComfyUI_EXO_LatentImageSize": ComfyUI_EXO_LatentImageSize
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI_EXO_LatentImageSize": "ComfyUI EXO Latent Image Size 👑"
}