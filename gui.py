import tkinter as tk
from tkinter import scrolledtext
import threading
from utils import respond, record_audio, speak

class DevProGUI:
    def __init__(self, root, respond_function, record_audio_function, speak_function, person_obj):
        self.root = root
        self.respond_function = respond_function
        self.record_audio_function = record_audio_function
        self.speak_function = speak_function
        self.person_obj = person_obj
        self.root.title("DevPro AI Voice Assistant")
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f0f0")

        # Conversation Display
        self.conversation_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', bg="#ffffff", fg="#000000", font=("Arial", 12))
        self.conversation_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # User Input Field
        self.input_field = tk.Entry(root, font=("Arial", 12))
        self.input_field.pack(pady=10, padx=10, fill=tk.X)
        self.input_field.bind("<Return>", self.process_input)

        # Buttons
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        self.voice_button = tk.Button(button_frame, text="🎤 Voice Input", command=self.start_voice_input, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.voice_button.pack(side=tk.LEFT, padx=5)

        self.text_button = tk.Button(button_frame, text="📝 Text Input", command=self.process_text_input, bg="#008CBA", fg="white", font=("Arial", 12))
        self.text_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(button_frame, text="❌ Exit", command=self.root.quit, bg="#f44336", fg="white", font=("Arial", 12))
        self.exit_button.pack(side=tk.LEFT, padx=5)

    def display_message(self, sender, message):
        """
        Display a message in the conversation area.
        """
        self.conversation_area.config(state='normal')
        self.conversation_area.insert(tk.END, f"{sender}: {message}\n")
        self.conversation_area.config(state='disabled')
        self.conversation_area.yview(tk.END)

    def process_input(self, event=None):
        """
        Process text input from the user.
        """
        user_input = self.input_field.get()
        if user_input.strip() == "":
            return
        self.display_message("You", user_input)
        self.input_field.delete(0, tk.END)
        threading.Thread(target=self.process_command, args=(user_input,)).start()

    def process_text_input(self):
        """
        Trigger text input processing.
        """
        self.process_input()

    def start_voice_input(self):
        """
        Start voice input in a separate thread.
        """
        threading.Thread(target=self.process_voice_input).start()

    def process_voice_input(self):
        """
        Process voice input from the user.
        """
        try:
            self.voice_button.config(state='disabled')  # Disable button while listening
            self.display_message("System", "🎤 Listening... Please speak now")
            self.root.update()  # Force GUI update
            
            voice_data = self.record_audio_function()
            
            if voice_data and voice_data.strip():
                self.display_message("You", voice_data)
                self.process_command(voice_data)
            else:
                self.display_message("System", "❌ No speech detected. Please try again.")
        except Exception as e:
            self.display_message("System", f"❌ Error: {str(e)}")
        finally:
            self.voice_button.config(state='normal')  # Re-enable button

    def process_command(self, command):
        """
        Process the command and display the assistant's response.
        """
        self.respond_function(command, self.person_obj, self.speak)

    def speak(self, audio_string):
        """
        Override the speak function to display the response in the GUI.
        """
        self.display_message("DevPro", audio_string)