# This class will allow the user to moddify the position of the text displayed in the text widget

import tkinter as tk
from RadioButtonGroup import RadioButtonGroup

class Justify:
    
    # Constructor
    def __init__(self, root, textWidget):
        self.__textWidget = textWidget                                                                   # This will be the text object
        radioButonConfig = {"command" : self.test,                                                       # This command will change the postion of text displayed using the poorly named test method
                            "indicator" : 0,                                                             # This will make radiobutton symbol disapear
                            "background" : "dark grey",                                                  # bg color
                            "activebackground" : "light blue",                                           # Actove bg color
                            "compound" : tk.TOP,                                                         # Show image above text
                            "selectcolor" : "light grey"}                                                # select color
        
        orientationOptions = {"Right" : "Right", "Center" : "Center", "Left" : "Left"}                   # Values for the radio button group
        orientationPhotos = {key : f"images/{key}.png" for (key, value) in orientationOptions.items()}   # Images that will relate to each choice

        self.__RGB = RadioButtonGroup(root = root,                                                       # Root where the RGB will  be displayed
                                      options = orientationOptions,                                      # These are options the user can chose
                                      radioButonConfig = radioButonConfig,                               # Use options defined above
                                      default = "Center",                                                # Default option (Center)
                                      name = "Orientation",                                              # Variable name
                                      parameterName = "variable",                                        # Name of the tkinter option
                                      showText = False).execute(fill = tk.BOTH,
                                                                ipadx = 0,
                                                                ipady = 0,
                                                                side = tk.RIGHT,
                                                                expand = True)
    # This command will change the postion of text displayed using the poorly named test method
    def test(self):
        justifyValue = self.__RGB.getValue()                                                             # Get the value of what the user chose
        self.__textWidget.tag_configure("center", justify = justifyValue.lower())                        # Create tag that will center the text displayed
        self.__textWidget.tag_add("center", "1.0", "end")                                                # Add this tag to widget