# DevPro AI Assistant

Welcome to the DevPro AI Assistant! This is a versatile, beginner-friendly personal voice assistant designed to provide an approachable entry point to AI and voice technologies. It's built with Python and focuses on practical speech recognition and automation features that you can easily customize and extend.

## Key Features

- **Voice Commands**: Interact naturally with the assistant through spoken language.
- **Application Control**: Open installed desktop applications via voice commands.
- **Web Search**: Search Google, Wikipedia, and YouTube using your voice.
- **Customizable**: Easily extend functionalities for additional commands or APIs.
- **Beginner-Friendly**: Clean, modular code with clear comments and documentation.

## Technology Stack

- **Python 3.x**: The core programming language.
- **SpeechRecognition**: For capturing and recognizing voice input.
- **gTTS (Google Text-to-Speech)**: For converting text responses into speech.
- **playsound**: For playing the generated audio files.
- **PyAudio**: For accessing the microphone.
- **wikipedia**: For easy integration with the Wikipedia API.
- **pywhatkit**: For interacting with YouTube.

## Project Structure

The project is organized as a proper Python package for better modularity and distribution:

```
DevPro-AI-Assistant/
├── devpro_ai_assistant/
│   ├── __init__.py
│   ├── __main__.py          # Main entry point for the application
│   ├── config/              # Configuration files
│   │   ├── __init__.py
│   │   └── settings.py      # Assistant settings (e.g., wake word)
│   └── modules/             # Core functionalities
│       ├── __init__.py
│       ├── speech_to_text.py
│       ├── text_to_speech.py
│       ├── command_handler.py
│       ├── app_launcher.py
│       └── web_search.py
├── tests/
│   └── test_initialization.py # Basic tests for the project
├── requirements.txt         # Project dependencies
└── README.md                # This file
```

## Setup and Installation

Follow these steps to set up the DevPro AI Assistant on your local machine.

### Prerequisites

- Python 3.7 or higher
- `pip` for package management
- A working microphone

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone <repository-url>
cd DevPro-AI-Assistant
```

### 2. Install System Dependencies

On some systems, particularly Debian/Ubuntu-based Linux distributions, you may need to install system-level dependencies for `PyAudio`.

```bash
sudo apt-get update && sudo apt-get install -y portaudio19-dev
```

For other operating systems, please refer to the `PyAudio` documentation for installation instructions.

### 3. Install Python Packages

Install all the required Python libraries using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## How to Run the Assistant

To start the assistant, run it as a module from the root of the project directory (`DevPro-AI-Assistant/`):

```bash
python -m devpro_ai_assistant
```

The assistant will greet you and then wait for you to say the wake word.

## Usage

1.  **Activate the Assistant**: Say the wake word, which is "assistant" by default. You can change this in `devpro_ai_assistant/config/settings.py`.
2.  **Give a Command**: Once the assistant responds with "Yes? How can I help you?", you can give a command, such as:
    - *"Open notepad"*
    - *"Search Google for the latest Python news"*
    - *"Search Wikipedia for Albert Einstein"*
    - *"Search YouTube for a Python tutorial"*
3.  **Exit the Assistant**: Say "goodbye", "exit", or "quit" to stop the application.

## Extensibility and Customization

This project is designed to be easily extended. Here are some ways you can customize it:

### Changing the Wake Word

You can change the wake word by editing the `WAKE_WORD` variable in `devpro_ai_assistant/config/settings.py`.

### Adding New Voice Commands

To add a new command, you'll need to:

1.  **Create a new module** in the `devpro_ai_assistant/modules/` directory for your new functionality (e.g., `email_sender.py`).
2.  **Implement the logic** in your new module. For example, a function `send_email(to, subject, body)`.
3.  **Update the command handler** (`devpro_ai_assistant/modules/command_handler.py`) to recognize a new voice command and call your new function.

```python
# In devpro_ai_assistant/modules/command_handler.py

from . import email_sender # Import your new module

def handle_command(command):
    # ... existing commands
    if 'send email' in command:
        # You'll need to parse the recipient, subject, etc. from the command
        text_to_speech.speak("Who should I send the email to?")
        recipient = speech_to_text.listen()
        # ... and so on
        # email_sender.send_email(...)
```

### Customizing Application Paths

The `devpro_ai_assistant/modules/app_launcher.py` module contains a basic mapping of application names to their executables. You can customize or expand this list to include the applications you use most often. For a more robust solution, consider moving this mapping to the `config/settings.py` file.

## Debugging

- **Microphone Issues**: If the assistant can't hear you, make sure your microphone is properly connected and configured as the default input device in your system settings. You can also adjust the `r.pause_threshold` in `devpro_ai_assistant/modules/speech_to_text.py` if the listener cuts off too early.
- **API Errors**: Ensure you have a stable internet connection, as both speech recognition and web search functionalities rely on it.
- **Dependency Problems**: If you encounter installation errors, make sure you have the latest version of `pip` and that all system dependencies (like `portaudio19-dev`) are correctly installed.

## Best Practices

- **Keep Modules Separate**: For each new major feature, create a new module to keep the code organized and easy to maintain.
- **Use a Configuration File**: Store settings, API keys, and other customizable parameters in the `config/` directory instead of hardcoding them in the scripts.
- **Error Handling**: Wrap external API calls and potentially problematic code in `try...except` blocks to handle errors gracefully.
- **Provide Feedback**: Use the `text_to_speech` module to give users feedback on what the assistant is doing (e.g., "Searching Google for...").

Enjoy building with your new AI assistant!