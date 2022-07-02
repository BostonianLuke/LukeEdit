# Child of widget, parent of Spinbox & RadioButtonGroup classess

from Widget import Widget
import tkinter as tk

class EntryWidget(Widget):
    
    def __init__(self, root, config, default, name, parameterName):                               
        self._root = root                                                                             # Root window                                                                       
        self._config = config                                                                         # Dict of widget specific settings 
        self.__name = name                                                                            # Name of the tkinter StringVar that will hold user entry data
        self._config[parameterName] = tk.StringVar(self._root, name = self.__name, value = default)   # Bind this StringVar to the config dict
        
    def getValue(self):
        return self._root.getvar(name = self.__name)   