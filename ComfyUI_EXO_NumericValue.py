class ComfyUI_EXO_NumericValue:
    """
    A simple numeric value node for numeric entry with a single float output.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Numeric_Value": ("FLOAT", {"default": 0.05, "step": 0.01, "tooltip": "Enter a numeric value for output"}),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("Numeric_Value",)
    FUNCTION = "process_float"
    CATEGORY = "Custom EXO Nodes"
    
    # Output tooltip using the correct format
    OUTPUT_TOOLTIPS = ("Connect this output to a node that expects a Numeric value for its input.",)

    def process_float(self, Numeric_Value):
        """
        Returns the entered float value.
        
        Args:
            Numeric_Value (float): The numeric input provided by the user.
        
        Returns:
            float: The entered numeric value.
        """
        return (Numeric_Value,)

# Register node mappings
NODE_CLASS_MAPPINGS = {
    "ComfyUI_EXO_NumericValue": ComfyUI_EXO_NumericValue,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI_EXO_NumericValue": "ComfyUI EXO Numeric Value 👑",
}