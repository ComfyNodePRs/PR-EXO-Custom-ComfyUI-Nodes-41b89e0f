import yaml
import os
import locale

# Custom directory for language files
LANGUAGE_DIR = os.path.join(os.path.dirname(__file__), "languages")

# Detect the system's default language
default_locale = locale.getdefaultlocale()[0]
if default_locale:
    default_language = default_locale.split('_')[0]
else:
    default_language = "en"

# Load language settings
def load_language_settings(language_code):
    language_file = f"{language_code}.yaml"
    with open(os.path.join(LANGUAGE_DIR, language_file), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

language_settings = load_language_settings(default_language)
