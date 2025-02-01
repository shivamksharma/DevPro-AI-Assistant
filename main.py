import time
import tkinter as tk
from tkinter import messagebox
import logging
from gui import DevProGUI
from utils import respond, record_audio, speak, test_microphone

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

class Person:
    def __init__(self):
        self.name = ''
    
    def setName(self, name):
        self.name = name
        logging.info(f"Name set to: {name}")

def main():
    try:
        logging.info("Starting DevPro AI Voice Assistant...")
        
        # Test microphone before starting
        logging.info("Testing microphone...")
        if not test_microphone():
            logging.error("Microphone not working or not properly configured")
            raise Exception("Microphone test failed. Please check your microphone settings.")
        
        # Initialize the GUI
        logging.info("Initializing GUI...")
        root = tk.Tk()
        root.title("DevPro AI Voice Assistant")
        
        # Set minimum window size
        root.minsize(600, 400)
        
        # Center the window on screen
        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        person_obj = Person()
        gui = DevProGUI(root, respond, record_audio, speak, person_obj)
        
        logging.info("GUI initialized successfully")
        root.mainloop()
        
    except Exception as e:
        logging.error(f"Error starting the application: {str(e)}")
        if 'root' in locals():
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            root.destroy()
        raise

if __name__ == "__main__":
    main()