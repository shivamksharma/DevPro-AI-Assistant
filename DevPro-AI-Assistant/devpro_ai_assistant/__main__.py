from .modules import speech_to_text, text_to_speech, command_handler
from .config import settings

def main():
    """
    Main function to run the DevPro AI Assistant.
    """
    text_to_speech.speak("DevPro AI Assistant is now active.")

    while True:
        # Listen for the wake word
        print(f"Waiting for wake word: '{settings.WAKE_WORD}'...")
        wake_word_query = speech_to_text.listen()

        if wake_word_query and settings.WAKE_WORD in wake_word_query:
            text_to_speech.speak("Yes? How can I help you?")

            # Listen for the actual command
            command = speech_to_text.listen()

            if command:
                # Exit condition
                if "goodbye" in command or "exit" in command or "quit" in command:
                    text_to_speech.speak("Goodbye!")
                    break

                # Handle the command
                command_handler.handle_command(command)
            else:
                text_to_speech.speak("Sorry, I didn't catch that. Please try again.")

if __name__ == "__main__":
    main()