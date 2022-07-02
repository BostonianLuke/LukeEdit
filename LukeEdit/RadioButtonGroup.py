import tkinter as tk
from PIL import Image, ImageTk
from EntryWidget import EntryWidget
from RadioButton import RadioButton

class RadioButtonGroup(EntryWidget):

    def __init__(self, root, options, radioButonConfig, default, name, parameterName, showText = True):          # Constructor for RadioButtonGroup class    
        self.__showText = showText                                                                                         # Flag that determines if text will be shown in button  
        super().__init__(root, radioButonConfig, default, name, parameterName)                                             # Constructor for EntryWidget class
        self.__options = options                                                                                           # Options thats determine's the text and val of each button
        self.__photoDict = {option : ImageTk.PhotoImage(file = f"images/{option}.png") for option in options.keys()}       # This dict will contain all the images inside radio button
        
    def execute(self, fill, ipadx, ipady, side, expand):      # This overide's the Widget's execute method 
        for (text, value) in self.__options.items():               # For each pair in the options dict
            self._config["value"] = value                          # Sets value as the val in dict
            self._config["image"] = self.__photoDict[text]         # Sets image for each radio button baeed on dict
            if self.__showText:                                    # If text flag is set to True:
                self._config["text"] = text                             # Add text from options dict, so that it's displayed in radio button
                
            # Create and add the radio button
            RadioButton(self._root).config(self._config).execute(fill = fill, ipadx = ipadx, ipady = ipady, side = side, expand = expand)
        return self