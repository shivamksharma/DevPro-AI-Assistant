import speech_recognition as sr
from gtts import gTTS
import random
import playsound
import os
import webbrowser
import yfinance as yf
import requests
from datetime import datetime
from weather import speak_weather

def record_audio(ask=False):
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.energy_threshold = 4000  # Adjust this value based on your microphone
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for background noise
        if ask:
            speak(ask)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            voice_data = r.recognize_google(audio)
            return voice_data.lower()
        except sr.WaitTimeoutError:
            return "Timeout: No speech detected"
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Could not connect to speech recognition service"
        except Exception as e:
            return f"Error: {str(e)}"

def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(f"devpro: {audio_string}")
    os.remove(audio_file)

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
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Testing microphone...")
            r.adjust_for_ambient_noise(source, duration=1)
            return True
    except Exception as e:
        print(f"Microphone test failed: {str(e)}")
        return False