"""
ComfyUI Custom Node for dynamic prompt building and template management.
Provides a modular system for combining prompt templates from multiple categories,
with support for positive and negative prompts.
"""

import json
import os
import platform  # Add this import statement
from collections import defaultdict
from global_flags import console_cleared

def clear_console():
    global console_cleared
    if not console_cleared:
        # Detect the operating system
        current_os = platform.system()

        # Clear the console based on the operating system
        if current_os == "Windows":
            os.system('cls')
        else:
            os.system('clear')

        # Set the flag to indicate the console has been cleared
        console_cleared = True

# Base configuration paths
base_dir = os.path.dirname(__file__)
config_path = os.path.join(base_dir, "prompt_builder_config.json")

# Load main configuration
try:
    with open(config_path, 'r', encoding='utf-8') as f:
        main_config = json.load(f)
except json.JSONDecodeError as e:
    print(f"\nError: Configuration file is malformed: {str(e)}")
    raise
except (PermissionError, IOError) as e:
    print(f"\nError: Unable to read configuration file: {str(e)}")
    raise

data_folder_path = os.path.join(base_dir, main_config["paths"]["data_folder"])

class Template:
    """Core template class for handling prompt text replacements and combinations"""
    def __init__(self, positive_prompt, negative_prompt, **kwargs):
        self.prompt = positive_prompt
        self.negative_prompt = negative_prompt

    def replace_prompts(self, positive_prompt, negative_prompt):
        """Combines template prompts with user input"""
        # Clean up user input - remove trailing commas and spaces
        positive_prompt = positive_prompt.strip().rstrip(',').strip()
        negative_prompt = negative_prompt.strip().rstrip(',').strip()
        
        # Ensure clean replacement without adding spaces
        positive_result = self.prompt.replace('{pos_prompt}', positive_prompt)
        negative_result = self.negative_prompt.replace('{neg_prompt}', negative_prompt)
        return positive_result.strip(), negative_result.strip()

class StylerData:
    """Manages prompt templates and their organization"""
    def __init__(self, custom_order, data_folder_path):
        self._data = defaultdict(dict)
        self.custom_order = custom_order

        if not os.path.exists(data_folder_path):
            print(f"\nError: Data folder not found: {data_folder_path}")
            return

        # Process available folders and files
        available_folders = os.listdir(data_folder_path)
        missing_files = []
        missing_folders = []

        # Load and sort JSON files based on custom order
        for folder_name in sorted(available_folders,
                                key=lambda x: self.custom_order.index(x) if x in self.custom_order else float('inf')):
            folder_path = os.path.join(data_folder_path, folder_name)

            if os.path.isdir(folder_path):
                json_file_path = os.path.join(folder_path, f"{folder_name}.json")
                if not os.path.exists(json_file_path):
                    missing_files.append(folder_name)
                    continue
                self._load_template_file(folder_path, folder_name)

        # Verify configuration integrity
        for section in main_config["sections"]:
            for folder in section["folders"]:
                if folder not in available_folders:
                    missing_folders.append(folder)

        # Report any issues found during initialization
        if missing_files:
            print(f"\nWarning: Missing JSON files in folders: {', '.join(missing_files)}")
        if missing_folders:
            print(f"\nWarning: Missing folders specified in config: {', '.join(missing_folders)}")

    def _load_template_file(self, folder_path, folder_name):
        """Loads and validates template files"""
        json_file_path = os.path.join(folder_path, f"{folder_name}.json")
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                for template in content:
                    if not all(key in template for key in ['name', 'positive_prompt', 'negative_prompt']):
                        print(f"\nWarning: Malformed template in {folder_name}.json - skipping entry")
                        continue
                    self._data[folder_name][template['name']] = Template(**template)
        except json.JSONDecodeError as e:
            print(f"\nWarning: JSON formatting error in {json_file_path}: {str(e)}")
        except (PermissionError, IOError) as e:
            print(f"\nWarning: Unable to read {json_file_path}: {str(e)}")

    def get_template(self, folder, name):
        """Template accessor method"""
        return self._data[folder].get(name)

    def __getitem__(self, item):
        return self._data[item]

    def keys(self):
        return self._data.keys()

# Initialize the styler data with configuration
styler_data = StylerData(custom_order=main_config.get("order", []), data_folder_path=data_folder_path)

class ComfyUI_EXO_PromptBuilderDeluxe:
    """
    A ComfyUI node that constructs prompts using a template-based system.
    Features section toggles and category selections for template combinations.
    Outputs both positive and negative prompts for downstream processing.
    """

    menus = tuple(styler_data.keys())

    @classmethod
    def INPUT_TYPES(cls):
        """Defines the node's input interface"""
        inputs = {
            "Positive_Prompt_Text": ("STRING", {"default": "", "multiline": True, "placeholder": "Positive Text:"}),
            "Negative_Prompt_Text": ("STRING", {"multiline": True, "placeholder": "Negative Text:"}),
            "log_prompt_to_console": ("BOOLEAN", {"default": False, "label_on": "Yes", "label_off": "No"})
        }

        # Generate section-specific inputs
        for section in main_config["sections"]:
            inputs[f"{section['toggle']}"] = ("BOOLEAN", {"default": True, "label_on": "Enabled", "label_off": "Disabled"})

            for folder in section["folders"]:
                if folder in styler_data.keys():
                    inputs[folder] = (list(styler_data[folder].keys()),)

        return {"required": inputs}

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("Positive_Prompt_Text", "Negative_Prompt_Text")
    OUTPUT_TOOLTIPS = (
        "Connect this output to another nodes text (STRING) input.",
        "Connect this output to another nodes text (STRING) input."
    )
    FUNCTION = "process"
    CATEGORY = "Custom EXO Nodes"

    def process(self, Positive_Prompt_Text, Negative_Prompt_Text, log_prompt_to_console, **kwargs):
        """Main processing method for prompt building"""
        # Clear the console (only once)
        # clear_console()
        
        

        combined_positive_prompt = Positive_Prompt_Text
        combined_negative_prompt = Negative_Prompt_Text
        added_entries = set()

        # Process each enabled section
        for section in main_config["sections"]:
            toggle_name = section["toggle"]
            section_enabled = kwargs.get(toggle_name, False)

            if section_enabled:
                for folder in section["folders"]:
                    if folder in styler_data.keys():
                        selection = kwargs.get(folder)

                        # Add selected template to prompt if not already added
                        if selection and selection not in added_entries:
                            selected_template = styler_data[folder].get(selection)
                            if selected_template:
                                section_positive, section_negative = selected_template.replace_prompts("", "")
                                # Only add space if both parts have content
                                if combined_positive_prompt and section_positive:
                                    # Clean up any trailing commas before adding new section
                                    combined_positive_prompt = combined_positive_prompt.strip().rstrip(',').strip()
                                    section_positive = section_positive.strip().rstrip(',').strip()
                                    combined_positive_prompt = f"{combined_positive_prompt}, {section_positive}"
                                else:
                                    combined_positive_prompt = combined_positive_prompt or section_positive.strip().rstrip(',').strip()
                                    
                                if combined_negative_prompt and section_negative:
                                    # Clean up any trailing commas before adding new section
                                    combined_negative_prompt = combined_negative_prompt.strip().rstrip(',').strip()
                                    section_negative = section_negative.strip().rstrip(',').strip()
                                    combined_negative_prompt = f"{combined_negative_prompt}, {section_negative}"
                                else:
                                    combined_negative_prompt = combined_negative_prompt or section_negative.strip().rstrip(',').strip()
                                added_entries.add(selection)

        # Clean up whitespace and ensure no trailing comma in final prompts
        combined_positive_prompt = combined_positive_prompt.strip().rstrip(',').strip() if combined_positive_prompt else ""
        combined_negative_prompt = combined_negative_prompt.strip().rstrip(',').strip() if combined_negative_prompt else ""

        if log_prompt_to_console:
            self._log_prompts(combined_positive_prompt, combined_negative_prompt)

        return combined_positive_prompt, combined_negative_prompt

    def _log_prompts(self, positive_prompt, negative_prompt):
        """Console output formatter for prompts"""
        GREEN, RED, RESET = "\033[92m", "\033[91m", "\033[0m"
        print("\n\n")
        print(f"{GREEN}Combined Positive Prompt:{RESET}")
        print(positive_prompt)
        print("\n\n")
        print(f"{RED}Combined Negative Prompt:{RESET}")
        print(negative_prompt)
        print("\n\n")

# Node registration
NODE_CLASS_MAPPINGS = {
    "ComfyUI_EXO_PromptBuilderDeluxe": ComfyUI_EXO_PromptBuilderDeluxe
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUI_EXO_PromptBuilderDeluxe": "ComfyUI EXO Prompt Builder Deluxe 👑"
}
