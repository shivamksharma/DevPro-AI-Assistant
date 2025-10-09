import tempfile
from gtts import gTTS
from playsound import playsound

def speak(text, lang='en'):
    """
    Converts text to speech and plays the audio using a temporary file.

    Args:
        text (str): The text to be spoken.
        lang (str): The language of the text.
    """
    try:
        tts = gTTS(text=text, lang=lang)
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as fp:
            tts.save(fp.name)
            playsound(fp.name)
    except Exception as e:
        print(f"Error in text-to-speech: {e}")