import os
import platform
from . import text_to_speech

def launch_app(app_name):
    """
    Launches a desktop application based on the operating system.
    This is a basic implementation and might need to be customized.
    """
    system = platform.system()
    app_name = app_name.lower()

    # A more robust solution would be to use a configuration file
    # to map app names to their executable paths.
    apps = {
        "windows": {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "chrome": "chrome.exe"
        },
        "linux": {
            "terminal": "gnome-terminal",
            "firefox": "firefox",
            "gedit": "gedit"
        },
        "darwin": { # macOS
            "terminal": "Terminal.app",
            "safari": "Safari.app",
            "textedit": "TextEdit.app"
        }
    }

    os_apps = apps.get(system.lower())
    if not os_apps:
        text_to_speech.speak(f"Sorry, I don't have application mappings for {system}.")
        return

    executable = os_apps.get(app_name)
    if not executable:
        text_to_speech.speak(f"Sorry, I don't know how to open {app_name}.")
        return

    try:
        if system == "Darwin":
            os.system(f"open -a {executable}")
        elif system == "Linux":
            os.system(f"{executable} &") # Run in background
        elif system == "Windows":
            os.system(f"start {executable}")
        else:
            text_to_speech.speak(f"Unsupported operating system: {system}")
            return

        text_to_speech.speak(f"Opening {app_name}")
    except Exception as e:
        text_to_speech.speak(f"Sorry, I could not open {app_name}. Error: {e}")