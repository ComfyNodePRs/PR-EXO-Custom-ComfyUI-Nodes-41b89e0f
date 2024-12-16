"""
ComfyUI Custom Node for displaying and passing through text content.
Provides a visual display of both positive and negative prompts while 
allowing the text to continue through the workflow.
"""

class ComfyUI_EXO_DisplayText:
    """
    A ComfyUI node that displays text content in the UI and passes it through.
    Shows both positive and negative prompts in a formatted display while
    maintaining the ability to connect to downstream nodes.
    """
    
    def __init__(self):
        self.type = "output"  # Marks this as a node with UI display capabilities

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Positive_Text": ("STRING", {
                    "forceInput": True, 
                    "multiline": True, 
                    "tooltip": "Connect this input to another nodes text (STRING) output."
                }),
                "Negative_Text": ("STRING", {
                    "forceInput": True, 
                    "multiline": True, 
                    "tooltip": "Connect this input to another nodes text (STRING) output."
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("Positive_Text", "Negative_Text")
    OUTPUT_TOOLTIPS = (
        "Connect this output to another nodes text (STRING) input.",
        "Connect this output to another nodes text (STRING) input."
    )
    OUTPUT_NODE = True
    FUNCTION = "process_text"
    CATEGORY = "Custom EXO Nodes"

    def process_text(self, Positive_Text, Negative_Text):
        """
        Processes and prepares text for both UI display and node outputs.
        
        Args:
            Positive_Text (str): The positive prompt text
            Negative_Text (str): The negative prompt text
            
        Returns:
            dict: Contains both UI display data and node output values
        """
        # Ensure proper UTF-8 encoding to handle special characters
        def ensure_utf8(text):
            if isinstance(text, bytes):
                return text.decode('utf-8')
            elif isinstance(text, str):
                return text.encode('utf-8').decode('utf-8')
            return text

        Positive_Text = ensure_utf8(Positive_Text)
        Negative_Text = ensure_utf8(Negative_Text)

        # Handle invalid inputs gracefully
        if Positive_Text is None or not isinstance(Positive_Text, str):
            Positive_Text = ""
        if Negative_Text is None or not isinstance(Negative_Text, str):
            Negative_Text = ""

        # Clean up text for display
        processed_positive_text = Positive_Text.strip()
        processed_negative_text = Negative_Text.strip()

        # Format text for UI display
        combined_text = ""
        if processed_positive_text:
            combined_text += f"{processed_positive_text}\n"
        else:
            combined_text += "No positive text provided\n"

        if processed_negative_text:
            combined_text += f"{processed_negative_text}"
        else:
            combined_text += "No negative text provided"

        return {
            "ui": {
                "text": combined_text,  # For node UI display
            },
            "result": (Positive_Text, Negative_Text),  # For node outputs
        }

    def UI(self, **kwargs):
        """
        Generates the HTML for displaying text in the node's UI.
        
        Args:
            kwargs: Contains UI data from process_text
            
        Returns:
            str: HTML formatted string for node display
        """
        rendered_text = kwargs.get("ui", {}).get("text", "No text available")
        return f"<div style='padding: 10px; border: 1px solid #ccc; white-space: pre-wrap;'>Displaying Text:<br>{rendered_text}</div>"

# Register the node with ComfyUI
NODE_CLASS_MAPPINGS = {
    "ComfyUI_EXO_DisplayText": ComfyUI_EXO_DisplayText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI_EXO_DisplayText": "ComfyUI EXO Display Text 👑",
}