import nodes
import comfy.model_sampling

class ComfyUI_EXO_ModelSamplingFlux:
    NAME = "ComfyUI EXO Model SamplingFlux 👑"
    CATEGORY = "Custom EXO Nodes"

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "model": ("MODEL",),
            "width": ("INT", {"forceInput": True}),  # Changed to force input connection
            "height": ("INT", {"forceInput": True}), # Changed to force input connection
            "max_shift": ("FLOAT", {
                "default": 1.15,
                "min": 0.0,
                "max": 100.0,
                "step": 0.01,
                "display": "number"
            }),
            "base_shift": ("FLOAT", {
                "default": 0.5,
                "min": 0.0,
                "max": 100.0,
                "step": 0.01,
                "display": "number"
            })
        }}

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "patch"

    def patch(self, model, width, height, max_shift, base_shift):
        """
        Patches the model with flux sampling parameters.
        
        Args:
            model: The input model to patch
            width: Image width from connected node
            height: Image height from connected node
            max_shift: Maximum shift value
            base_shift: Base shift value
        
        Returns:
            tuple: Contains the patched model
        """
        m = model.clone()

        # Constants from original implementation
        x1 = 256
        x2 = 4096
        
        # Calculate shift using the same formula as original
        mm = (max_shift - base_shift) / (x2 - x1)
        b = base_shift - mm * x1
        shift = (width * height / (8 * 8 * 2 * 2)) * mm + b

        # Set up the sampling classes
        sampling_base = comfy.model_sampling.ModelSamplingFlux
        sampling_type = comfy.model_sampling.CONST

        class ModelSamplingAdvanced(sampling_base, sampling_type):
            pass

        # Create and configure the model sampling
        model_sampling = ModelSamplingAdvanced(model.model.model_config)
        model_sampling.set_parameters(shift=shift)
        
        # Add the sampling patch to the model
        m.add_object_patch("model_sampling", model_sampling)
        
        return (m,)

# Node class and display name mappings
NODE_CLASS_MAPPINGS = {
    "ComfyUI_EXO_ModelSamplingFlux": ComfyUI_EXO_ModelSamplingFlux
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI_EXO_ModelSamplingFlux": "ComfyUI EXO Model SamplingFlux 👑"
}