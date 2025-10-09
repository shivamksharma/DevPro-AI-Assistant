import webbrowser
import wikipedia
from . import text_to_speech

def google_search(query):
    """
    Performs a Google search for the given query.
    """
    try:
        text_to_speech.speak(f"Searching Google for {query}")
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
    except Exception as e:
        text_to_speech.speak(f"Sorry, I could not perform the Google search. Error: {e}")

def wikipedia_search(query):
    """
    Performs a Wikipedia search and speaks the summary.
    """
    try:
        text_to_speech.speak(f"Searching Wikipedia for {query}")
        results = wikipedia.summary(query, sentences=2)
        text_to_speech.speak("According to Wikipedia...")
        text_to_speech.speak(results)
    except wikipedia.exceptions.PageError:
        text_to_speech.speak(f"Sorry, I could not find any results for {query} on Wikipedia.")
    except wikipedia.exceptions.DisambiguationError as e:
        text_to_speech.speak(f"There are multiple results for {query}. Please be more specific. Options are: {e.options[:3]}")
    except Exception as e:
        text_to_speech.speak(f"Sorry, I could not perform the Wikipedia search. Error: {e}")

def youtube_search(query):
    """
    Searches for a video on YouTube and plays the first result.
    """
    try:
        import pywhatkit
        text_to_speech.speak(f"Searching YouTube for {query}")
        pywhatkit.playonyt(query)
    except Exception as e:
        text_to_speech.speak(f"Sorry, I could not perform the YouTube search. Error: {e}")