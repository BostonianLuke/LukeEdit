# Child of widget, wrapper class for Tkinter's Entry class

import tkinter as tk
from Widget import Widget

class Entry(Widget):
    
    def __init__(self, root):
        self._widget = tk.Entry(root)   # Constrcutor assigns widget var to tkinter's Entry class object
        self._widget.focus_force()      # Force cursor to highlight input area
        
    def getInput(self):
        return self._widget.get()       # Getter for user input