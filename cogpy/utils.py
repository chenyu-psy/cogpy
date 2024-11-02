from pathlib import Path
import tkinter as tk


#%% Create a hidden Tkinter root window once, at module load time
root = tk.Tk()
root.withdraw()  # Hide the main window

def is_capslock_on():
    """Check if Caps Lock is currently on."""
    return root.tk.call('tk::capslock')
