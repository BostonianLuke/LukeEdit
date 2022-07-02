# Child of widget, wrapper class for Tkinter's Label class

import tkinter as tk
from Widget import Widget

class Label(Widget):
    
    def __init__(self, root):
        self._widget = tk.Label(root)     # Constrcutor assigns widget var to tkinter's Label class object