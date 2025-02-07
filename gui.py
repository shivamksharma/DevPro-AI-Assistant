import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import threading
import logging
from utils import respond, record_audio, speak
import time
import concurrent.futures

class DevProGUI:
    def __init__(self, root, respond_function, record_audio_function, speak_function, person_obj):
        self.root = root
        self.respond_function = respond_function
        self.record_audio_function = record_audio_function
        self.speak_function = speak_function
        self.person_obj = person_obj
        
        # Configure main window
        self.root.configure(bg="#f0f0f0")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Style configuration
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f0f0f0")
        
        # Conversation Display with custom font and colors
        self.conversation_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=("Helvetica", 12),
            bg="#ffffff",
            fg="#000000",
            padx=10,
            pady=10
        )
        self.conversation_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.conversation_area.config(state='disabled')
        
        # Input area frame
        input_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # User Input Field with custom font
        self.input_field = ttk.Entry(
            input_frame,
            font=("Helvetica", 12),
            style="Custom.TEntry"
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self.process_input)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        button_frame.pack(fill=tk.X)
        
        # Custom button style
        style.configure(
            "Custom.TButton",
            font=("Helvetica", 11),
            padding=6
        )
        
        # Voice Input Button
        self.voice_button = ttk.Button(
            button_frame,
            text="🎤 Voice Input",
            command=self.start_voice_input,
            style="Custom.TButton"
        )
        self.voice_button.pack(side=tk.LEFT, padx=5)
        
        # Text Input Button
        self.text_button = ttk.Button(
            button_frame,
            text="📝 Send",
            command=self.process_text_input,
            style="Custom.TButton"
        )
        self.text_button.pack(side=tk.LEFT, padx=5)
        
        # Exit Button
        self.exit_button = ttk.Button(
            button_frame,
            text="❌ Exit",
            command=self.on_exit,
            style="Custom.TButton"
        )
        self.exit_button.pack(side=tk.RIGHT, padx=5)
        
        # Add continuous listening checkbox
        self.continuous_listening_var = tk.BooleanVar()
        ttk.Checkbutton(button_frame, text="Continuous Listen", 
                       variable=self.continuous_listening_var).pack(side=tk.LEFT)
        
        # Initial greeting
        self.display_message("System", "👋 Welcome to DevPro AI Assistant! Click the microphone button or type to begin.")
    
    def display_message(self, sender, message):
        """Display a message in the conversation area."""
        try:
            self.conversation_area.config(state='normal')
            timestamp = self.get_timestamp()
            formatted_message = f"[{timestamp}] {sender}: {message}\n\n"
            self.conversation_area.insert(tk.END, formatted_message)
            self.conversation_area.see(tk.END)
            self.conversation_area.config(state='disabled')
            self.root.update()
        except Exception as e:
            logging.error(f"Error displaying message: {str(e)}")
    
    def get_timestamp(self):
        """Get current timestamp for messages."""
        return time.strftime("%H:%M:%S")
    
    def process_input(self, event=None):
        """Process text input from the user."""
        user_input = self.input_field.get().strip()
        if not user_input:
            return
            
        self.input_field.delete(0, tk.END)
        self.display_message("You", user_input)
        threading.Thread(target=self.process_command, args=(user_input,), daemon=True).start()
    
    def process_text_input(self):
        """Trigger text input processing."""
        self.process_input()
    
    def start_voice_input(self):
        """Start voice input in a separate thread."""
        threading.Thread(target=self.process_voice_input, daemon=True).start()
    
    def process_voice_input(self):
        """Process voice input from the user."""
        try:
            self.voice_button.config(state='disabled')
            self.display_message("System", "🎤 Listening... Please speak now")
            
            voice_data = self.record_audio_function()
            
            if voice_data:
                if any(error_msg in voice_data.lower() for error_msg in ["error", "timeout", "could not"]):
                    self.display_message("System", f"❌ {voice_data}")
                else:
                    self.display_message("You", voice_data)
                    self.process_command(voice_data)
            else:
                self.display_message("System", "❌ No speech detected. Please try again.")
                
        except Exception as e:
            logging.error(f"Error in voice input: {str(e)}")
            self.display_message("System", f"❌ Error: {str(e)}")
        finally:
            self.voice_button.config(state='normal')
    
    def process_command(self, command):
        """Process the command and display the assistant's response."""
        try:
            self.display_message("System", "🤔 Processing...")
            # Use proper threading with error handling
            threading.Thread(
                target=self.respond_function,
                args=(command, self.person_obj, self.speak),
                daemon=True
            ).start()
        except Exception as e:
            logging.error(f"Error processing command: {str(e)}")
            self.display_message("System", f"❌ Error: {str(e)}")
    
    def speak(self, audio_string):
        """Override the speak function to display the response in the GUI."""
        self.display_message("DevPro", audio_string)
        try:
            self.speak_function(audio_string)
        except Exception as e:
            logging.error(f"Error in text-to-speech: {str(e)}")
    
    def on_exit(self):
        """Handle exit button click."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.quit()
    
    def handle_response(self, future):
        """Handle the response from the thread pool"""
        try:
            response = future.result()
            self.display_message("Assistant", response)
        except Exception as e:
            logging.error(f"Response error: {str(e)}")
            self.display_message("System", f"❌ Error: {str(e)}")