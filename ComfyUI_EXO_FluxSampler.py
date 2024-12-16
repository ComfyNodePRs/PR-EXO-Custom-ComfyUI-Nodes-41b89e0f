import comfy.samplers
import torch
import comfy.sample
import random
import comfy.model_sampling
import node_helpers
from nodes import EmptyLatentImage

class ComfyUI_EXO_FluxSampler:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "conditioning": ("CONDITIONING",),
                "width": ("INT", {"forceInput": True}),
                "height": ("INT", {"forceInput": True}),
                # NOISE section
                "noise_seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "increment_value": ("INT", {"default": 1, "min": 1, "max": 10000, "step": 1}),
                # SAMPLER section
                "sampler_name": (comfy.samplers.SAMPLER_NAMES,),
                # SCHEDULER section
                "scheduler": (comfy.samplers.SCHEDULER_NAMES,),
                "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                # Additional parameters
                "max_shift": ("FLOAT", {"default": 0.70, "min": 0.0, "max": 100.0, "step": 0.01}),
                "base_shift": ("FLOAT", {"default": 0.30, "min": 0.0, "max": 100.0, "step": 0.01}),
                "guidance": ("FLOAT", {"default": 2.0, "min": 0.0, "max": 100.0, "step": 0.1}),
            },
            "optional": {
                "negative_conditioning": ("CONDITIONING",),
            }
        }
    
    RETURN_TYPES = ("MODEL", "NOISE", "SAMPLER", "SIGMAS", "SEED", "LATENT", "GUIDER", "CONDITIONING")
    RETURN_NAMES = ("model_out", "noise", "sampler", "sigmas", "seed", "latent", "guider", "conditioning_out")
    FUNCTION = "generate"
    CATEGORY = "Custom EXO Nodes"

    def generate(self, model, conditioning, width, height, noise_seed, increment_value, 
                sampler_name, scheduler, steps, denoise, max_shift, base_shift, guidance,
                negative_conditioning=None):
        # Handle edge cases
        noise_seed = max(0, noise_seed)
        increment_value = max(1, increment_value)

        # Use provided negative conditioning or default to positive conditioning
        negative = negative_conditioning if negative_conditioning is not None else conditioning

        # Model Sampling Flux logic
        m = model.clone()
        x1 = 256
        x2 = 4096
        mm = (max_shift - base_shift) / (x2 - x1)
        b = base_shift - mm * x1
        shift = (width * height / (8 * 8 * 2 * 2)) * mm + b

        # Set up model sampling
        sampling_base = comfy.model_sampling.ModelSamplingFlux
        sampling_type = comfy.model_sampling.CONST

        class ModelSamplingAdvanced(sampling_base, sampling_type):
            pass

        model_sampling = ModelSamplingAdvanced(model.model.model_config)
        model_sampling.set_parameters(shift=shift)
        m.add_object_patch("model_sampling", model_sampling)

        # Generate sigmas using scheduler
        total_steps = steps
        if denoise < 1.0:
            if denoise <= 0.0:
                sigmas = torch.FloatTensor([])
            else:
                total_steps = int(steps/denoise)
        
        sigmas = comfy.samplers.calculate_sigmas(
            model.get_model_object("model_sampling"), 
            scheduler, 
            total_steps
        ).cpu()
        
        if denoise < 1.0:
            sigmas = sigmas[-(steps + 1):]

        # Create sampler object
        sampler = comfy.samplers.sampler_object(sampler_name)

        # Create noise generator
        class NoiseGenerator:
            def __init__(self, seed):
                self.seed = seed
            
            def generate_noise(self, input_latent):
                latent_image = input_latent["samples"]
                batch_inds = input_latent["batch_index"] if "batch_index" in input_latent else None
                return comfy.sample.prepare_noise(latent_image, self.seed, batch_inds)

        noise = NoiseGenerator(noise_seed)

        # Create seed dictionary for SEED type output
        seed_dict = {"seed": noise_seed}

        # Create latent using EmptyLatentImage
        latent = EmptyLatentImage().generate(width, height, batch_size=1)[0]

        # Create basic guider
        class Guider_Basic(comfy.samplers.CFGGuider):
            def set_conds(self, positive):
                self.inner_set_conds({"positive": positive})

        guider = Guider_Basic(model)
        guider.set_conds(conditioning)

        # Apply guidance to conditioning (from FluxGuidance)
        conditioning_out = node_helpers.conditioning_set_values(conditioning, {"guidance": guidance})

        # Return all outputs
        return (m, noise, sampler, sigmas, seed_dict, latent, guider, conditioning_out)

NODE_CLASS_MAPPINGS = {
    "ComfyUI_EXO_FluxSampler": ComfyUI_EXO_FluxSampler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI_EXO_FluxSampler": "ComfyUI EXO FluxSampler 👑"
}