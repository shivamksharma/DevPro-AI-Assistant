from . import text_to_speech
from . import app_launcher
from . import web_search

def handle_command(command):
    """
    Parses the command and delegates to the appropriate module.
    """
    if 'open' in command:
        app_name = command.replace('open', '').strip()
        app_launcher.launch_app(app_name)
    elif 'search google for' in command:
        query = command.replace('search google for', '').strip()
        web_search.google_search(query)
    elif 'search wikipedia for' in command:
        query = command.replace('search wikipedia for', '').strip()
        web_search.wikipedia_search(query)
    elif 'search youtube for' in command:
        query = command.replace('search youtube for', '').strip()
        web_search.youtube_search(query)
    else:
        text_to_speech.speak("I'm not sure how to handle that command.")