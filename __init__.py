import os
import platform
import sys

# Print ASCII art to console before loading node mappings
def display_ascii_art():
    ascii_art = """
\033[33m          )      )        )     )  (           (     
\033[33m       ( /(   ( /(     ( /(  ( /(  )\ )        )\ )  
\033[33m (     )\())  )\())    )\()) )\())(()/(   (   (()/(  
\033[33m )\   ((_)\  ((_)\    ((_)\ ((_)\  /(_))  )\   /(_)) 
\033[33m((\033[35m_\033[33m)  __((_)   ((_)   \033[35m _\033[33m((\033[35m_\033[33m)  ((_)(_))_  ((_) (_))   
\033[35m| __|\033[31m \ \/ /  / _ \   \033[35m| \| |\033[31m / _ \ |   \ | __|/ __|  
\033[35m| _|\033[31m   >  <  | (_) |  \033[35m| .` |\033[31m| (_) || |) || _| \__ \  
\033[35m|___|\033[31m /_/\_\  \___/   \033[35m|_|\_|\033[31m \___/ |___/ |___||___/    \033[0m                                                           

\033[31m...Loading EXO Node's\033[0m
""" 
    print(ascii_art)
display_ascii_art()

# Append the directory of the current file to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import nodes
from .ComfyUI_EXO_PromptBuilderDeluxe import NODE_CLASS_MAPPINGS as DeluxeMappings, NODE_DISPLAY_NAME_MAPPINGS as DeluxeDisplayNames
from .ComfyUI_EXO_DisplayText import NODE_CLASS_MAPPINGS as DisplayTextMappings, NODE_DISPLAY_NAME_MAPPINGS as DisplayTextDisplayNames
from .ComfyUI_EXO_SaveText import NODE_CLASS_MAPPINGS as SaveTextMappings, NODE_DISPLAY_NAME_MAPPINGS as SaveTextDisplayNames
from .ComfyUI_EXO_Clip_Text_Encode import NODE_CLASS_MAPPINGS as ClipTextMappings, NODE_DISPLAY_NAME_MAPPINGS as ClipTextDisplayNames
from .ComfyUI_EXO_NumericValue import NODE_CLASS_MAPPINGS as NumericValueMappings, NODE_DISPLAY_NAME_MAPPINGS as NumericValueDisplayNames
from .ComfyUI_EXO_ImageRescale import NODE_CLASS_MAPPINGS as ImageRescaleMappings, NODE_DISPLAY_NAME_MAPPINGS as ImageRescaleDisplayNames
from .ComfyUI_EXO_LatentImageSize import NODE_CLASS_MAPPINGS as LatentImageSizeMappings, NODE_DISPLAY_NAME_MAPPINGS as LatentImageSizeDisplayNames
from .ComfyUI_EXO_LatentImageSizeX import NODE_CLASS_MAPPINGS as LatentImageSizeXMappings, NODE_DISPLAY_NAME_MAPPINGS as LatentImageSizeXDisplayNames
from .ComfyUI_EXO_TranslateText import NODE_CLASS_MAPPINGS as TranslateTextMappings, NODE_DISPLAY_NAME_MAPPINGS as TranslateTextDisplayNames
from .ComfyUI_EXO_Notes import NODE_CLASS_MAPPINGS as NotesMappings, NODE_DISPLAY_NAME_MAPPINGS as NotesDisplayNames
from .ComfyUI_EXO_Model_SamplingFlux import NODE_CLASS_MAPPINGS as ModelSamplingFluxMappings, NODE_DISPLAY_NAME_MAPPINGS as ModelSamplingFluxDisplayNames
from .ComfyUI_EXO_FluxSampler import NODE_CLASS_MAPPINGS as FluxSamplerMappings, NODE_DISPLAY_NAME_MAPPINGS as FluxSamplerDisplayNames

# Initialize NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Update mappings with existing nodes
NODE_CLASS_MAPPINGS.update(DeluxeMappings)
NODE_CLASS_MAPPINGS.update(DisplayTextMappings)
NODE_CLASS_MAPPINGS.update(SaveTextMappings)
NODE_CLASS_MAPPINGS.update(ClipTextMappings)
NODE_CLASS_MAPPINGS.update(NumericValueMappings)
NODE_CLASS_MAPPINGS.update(ImageRescaleMappings)
NODE_CLASS_MAPPINGS.update(LatentImageSizeMappings)
NODE_CLASS_MAPPINGS.update(LatentImageSizeXMappings)
NODE_CLASS_MAPPINGS.update(TranslateTextMappings)
NODE_CLASS_MAPPINGS.update(NotesMappings)
NODE_CLASS_MAPPINGS.update(ModelSamplingFluxMappings)
NODE_CLASS_MAPPINGS.update(FluxSamplerMappings)

# Update display names for all nodes
NODE_DISPLAY_NAME_MAPPINGS.update(DeluxeDisplayNames)
NODE_DISPLAY_NAME_MAPPINGS.update(DisplayTextDisplayNames)
NODE_DISPLAY_NAME_MAPPINGS.update(SaveTextDisplayNames)
NODE_DISPLAY_NAME_MAPPINGS.update(ClipTextDisplayNames)
NODE_DISPLAY_NAME_MAPPINGS.update(NumericValueDisplayNames)
NODE_DISPLAY_NAME_MAPPINGS.update(ImageRescaleDisplayNames)
NODE_DISPLAY_NAME_MAPPINGS.update(LatentImageSizeDisplayNames)
NODE_DISPLAY_NAME_MAPPINGS.update(LatentImageSizeXDisplayNames)
NODE_DISPLAY_NAME_MAPPINGS.update(TranslateTextDisplayNames)
NODE_DISPLAY_NAME_MAPPINGS.update(NotesDisplayNames)
NODE_DISPLAY_NAME_MAPPINGS.update(ModelSamplingFluxDisplayNames)
NODE_DISPLAY_NAME_MAPPINGS.update(FluxSamplerDisplayNames)

# Set web directory for loading JavaScript
WEB_DIRECTORY = "./web"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
