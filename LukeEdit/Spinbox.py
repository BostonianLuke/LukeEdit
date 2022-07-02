# Child of EntryWidget, which is a child of Widget class. This is a wrapper class for Tkinter's Spinbox class

import tkinter as tk
from EntryWidget import EntryWidget

class Spinbox(EntryWidget):
    
    def __init__(self, root, spinboxConfig, default, name, parameterName):  # Constuctor for Spinbox class
        super().__init__(root, spinboxConfig, default, name, parameterName)     # Constructor for EntryWidget class
        self._widget = tk.Spinbox(root)                                         # Set widget to be Tkinter's Spinbox's