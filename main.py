import time
import tkinter as tk
from gui import DevProGUI
from utils import respond, record_audio, speak, test_microphone

class person:
    name = ''
    def setName(self, name):
        self.name = name

time.sleep(1)

person_obj = person()

if __name__ == "__main__":
    # Test microphone before starting
    if not test_microphone():
        print("Error: Microphone not working or not properly configured")
        exit(1)
        
    # Initialize the GUI
    root = tk.Tk()
    gui = DevProGUI(root, respond, record_audio, speak, person_obj)
    root.mainloop()