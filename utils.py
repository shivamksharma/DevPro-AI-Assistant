import speech_recognition as sr
from gtts import gTTS
import random
import playsound
import os
import webbrowser
import yfinance as yf
import requests
from datetime import datetime
import logging
from weather import speak_weather
import tempfile

def record_audio(ask=False, max_retries=3):
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.energy_threshold = 4000  # Optimized for different environments
    r.pause_threshold = 0.8
    r.non_speaking_duration = 0.3
    
    for attempt in range(max_retries + 1):
        try:
            with sr.Microphone() as source:
                logging.info(f"Attempt {attempt + 1}/{max_retries + 1}: Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source, duration=2)  # Increased duration
                
                if ask:
                    speak(ask)
                
                logging.info("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=7)
                
                logging.info("Recognizing speech...")
                voice_data = r.recognize_google(audio)
                logging.info(f"Recognized: {voice_data}")
                
                return voice_data.lower()
                
        except sr.WaitTimeoutError:
            if attempt < max_retries:
                logging.warning(f"Timeout on attempt {attempt + 1}. Retrying...")
                continue
            return "Timeout: No speech detected. Please try again."
        except sr.UnknownValueError:
            if attempt < max_retries:
                logging.warning(f"Could not understand speech on attempt {attempt + 1}. Retrying...")
                continue
            return "Sorry, I couldn't understand that. Please try again."
        except sr.RequestError as e:
            logging.error(f"Could not connect to speech recognition service: {str(e)}")
            return f"Could not connect to speech recognition service. Error: {str(e)}"
        except Exception as e:
            logging.error(f"Error in record_audio: {str(e)}")
            return f"An error occurred: {str(e)}"

def speak(audio_string):
    try:
        # Create a temporary directory for audio files if it doesn't exist
        temp_dir = os.path.join(tempfile.gettempdir(), 'devpro_audio')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate audio file
        tts = gTTS(text=audio_string, lang='en')
        audio_file = os.path.join(temp_dir, f'audio_{random.randint(1, 20000000)}.mp3')
        
        # Save and play
        tts.save(audio_file)
        playsound.playsound(audio_file)
        
        # Clean up
        os.remove(audio_file)
        
        logging.info(f"TTS: {audio_string}")
        
    except Exception as e:
        logging.error(f"Error in text-to-speech: {str(e)}")
        print(f"DevPro: {audio_string}")  # Fallback to text-only output

def there_exists(terms, voice_data):
    for term in terms:
        if term in voice_data:
            return True
    return False

def log_conversation(user_input, assistant_response):
    """
    Log user input and assistant response to a file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("conversation_history.txt", "a") as file:
        file.write(f"[{timestamp}] User: {user_input}\n")
        file.write(f"[{timestamp}] Assistant: {assistant_response}\n")

def respond(voice_data, person_obj):
    if there_exists(['hey', 'hi', 'hello', 'bonjour', 'hola'], voice_data):
        greetings = [f"hey, how can I help you to test this assistant application {person_obj.name}", f"hey, what's up? {person_obj.name}", f"I'm listening {person_obj.name}", f"how can I help you? {person_obj.name}", f"hello {person_obj.name}"]
        greet = greetings[random.randint(0, len(greetings) - 1)]
        speak(greet) 
        
    if there_exists(["what is your name", "what's your name", "tell me your name"], voice_data):
        if person_obj.name:
            speak("my name is Devprogramming")
        else:
            speak("my name is Devprogramming. what's your name?")

    if there_exists(["my name is"], voice_data):
        person_name = voice_data.split("is")[-1].strip()
        speak(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name)
        
    if there_exists(["how are you", "how are you doing"], voice_data):
        speak(f"I'm very well, thanks for asking {person_obj.name}")

    if there_exists(["what's the time", "tell me the time", "what time is it"], voice_data):
        time = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time}")
        
    if there_exists(["search for"], voice_data) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on google')

    if there_exists(["youtube"], voice_data):
        search_term = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on youtube')

    if there_exists(["price of"], voice_data):
        search_term = voice_data.lower().split(" of ")[-1].strip()
        stocks = {
            "apple": "AAPL",
            "microsoft": "MSFT",
            "facebook": "FB",
            "tesla": "TSLA",
            "bitcoin": "BTC-USD"
        }
        try:
            stock = stocks[search_term]
            stock = yf.Ticker(stock)
            price = stock.info["regularMarketPrice"]
            speak(f'price of {search_term} is {price} {stock.info["currency"]} {person_obj.name}')
        except:
            speak('oops, something went wrong')

    if there_exists(["weather in"], voice_data):
        city = voice_data.split("in")[-1].strip()
        speak_weather(city, speak)

    if there_exists(["exit", "quit", "goodbye"], voice_data):
        speak("going offline")
        exit()

    # Log the conversation
    log_conversation(voice_data, "Assistant response logged.")

def test_microphone():
    """Test microphone and audio setup."""
    try:
        logging.info("Testing microphone...")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=2)
            
            # Try to record a short sample to verify microphone is working
            logging.info("Recording short test sample...")
            audio = r.listen(source, timeout=3, phrase_time_limit=3)
            
            # Try to recognize the audio (even if no words were spoken)
            try:
                r.recognize_google(audio)
            except sr.UnknownValueError:
                # This is expected if no words were spoken
                pass
            
            logging.info("Microphone test successful")
            return True
    except Exception as e:
        logging.error(f"Microphone test failed: {str(e)}")
        return False