"""
ComfyUI Custom Node for encoding text prompts using CLIP models.
Handles both positive and negative prompts, producing conditioning 
tensors needed for image generation.
"""

class ComfyUI_EXO_Clip_Text_Encode:
    """
    A ComfyUI node that encodes text prompts into CLIP embeddings.
    Processes both positive and negative prompts and returns their 
    conditioning tensors along with the original text.
    """
    
    def __init__(self):
        self.type = "function"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Clip_Input": ("CLIP", {
                    "tooltip": "Connect this to a loaded CLIP model output."
                }),
                "Positive_Text": ("STRING", {
                    "multiline": True, 
                    "forceInput": True, 
                    "tooltip": "Connect this input to another nodes text (STRING) output."
                }),
                "Negative_Text": ("STRING", {
                    "multiline": True, 
                    "forceInput": True, 
                    "tooltip": "Connect this input to another nodes text (STRING) output."
                }),
            }
        }

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", "STRING", "STRING")
    RETURN_NAMES = ("Clip_Cond_Positive", "Clip_Cond_Negative", "Positive_Text", "Negative_Text")
    OUTPUT_TOOLTIPS = (
        "Connect this conditioning output to nodes that accept positive conditioning.",
        "Connect this conditioning output to nodes that accept negative conditioning.",
        "Connect this output to another nodes text (STRING) input.",
        "Connect this output to another nodes text (STRING) input."
    )
    FUNCTION = "encode_text"
    CATEGORY = "Custom EXO Nodes"

    def encode_text(self, Clip_Input, Positive_Text, Negative_Text):
        """
        Encodes positive and negative text prompts into CLIP embeddings.
        
        Args:
            Clip_Input: The CLIP model used for encoding
            Positive_Text (str): The positive prompt text
            Negative_Text (str): The negative prompt text
            
        Returns:
            tuple: (positive_conditioning, negative_conditioning, positive_text, negative_text)
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

        # Convert text to tokens for CLIP processing
        positive_tokens = Clip_Input.tokenize(Positive_Text)
        negative_tokens = Clip_Input.tokenize(Negative_Text)

        # Generate embeddings from tokens
        positive_output = Clip_Input.encode_from_tokens(positive_tokens, return_pooled=True, return_dict=True)
        negative_output = Clip_Input.encode_from_tokens(negative_tokens, return_pooled=True, return_dict=True)

        # Extract the primary conditioning tensors
        cond_positive = positive_output.pop("cond")
        cond_negative = negative_output.pop("cond")

        return (
            [[cond_positive, positive_output]], 
            [[cond_negative, negative_output]], 
            Positive_Text, 
            Negative_Text
        )

# Register the node with ComfyUI
NODE_CLASS_MAPPINGS = {
    "ComfyUI_EXO_Clip_Text_Encode": ComfyUI_EXO_Clip_Text_Encode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI_EXO_Clip_Text_Encode": "ComfyUI EXO Clip Text Encode 👑",
}