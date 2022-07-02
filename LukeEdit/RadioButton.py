# Child of widget, wrapper class for Tkinter's Radiobutton class

import tkinter as tk
from Widget import Widget

class RadioButton(Widget):
    
    def __init__(self, root):
        self._widget = tk.Radiobutton(root)    # Constrcutor assigns widget var to tkinter's Radiobutton class object