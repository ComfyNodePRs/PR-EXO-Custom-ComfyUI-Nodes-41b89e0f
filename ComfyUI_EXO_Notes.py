"""
ComfyUI Notes Node
A simple text entry node that allows adding multiline notes and documentation 
directly within ComfyUI workflows. Useful for documenting settings, configurations,
and workflow-specific notes.
"""

class ComfyUI_EXO_Notes:
    """
    Displays multiline text notes in ComfyUI workflows.
    Functions as an output node since it only displays information.
    """
    
    def __init__(self):
        self.type = "output"

    @classmethod
    def INPUT_TYPES(s):
        """
        Defines the input interface for the notes node.
        Creates a multiline text area for entering notes.
        """
        return {
            "required": {
                "Notes_Text": ("STRING", {
                    "multiline": True,
                    "default": "Enter your notes here...",
                    "tooltip": "Enter any notes or documentation for your workflow here."
                }),
            }
        }
    
    RETURN_TYPES = ()
    FUNCTION = "display_notes"
    CATEGORY = "Custom EXO Nodes"
    OUTPUT_NODE = True

    def display_notes(self, Notes_Text):
        """
        Displays the notes text in the ComfyUI interface.
        Returns a UI update dictionary containing the text to display.
        """
        return {
            "ui": {
                "text": Notes_Text
            },
        }

# Register the node with ComfyUI
NODE_CLASS_MAPPINGS = {
    "ComfyUI_EXO_Notes": ComfyUI_EXO_Notes,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI_EXO_Notes": "ComfyUI EXO Notes 👑",
}
