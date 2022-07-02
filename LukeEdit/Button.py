# Child of widget, wrapper class for Tkinter's Button class

import tkinter as tk
from Widget import Widget

class Button(Widget):
    
    def __init__(self, root):
        self._widget = tk.Button(root)    # Constrcutor assigns widget var to tkinter's Button class object