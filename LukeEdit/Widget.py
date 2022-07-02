# Parent of all GUI Widget Types

import tkinter as tk

class Widget:
        
    def config(self, configDict):                          # This method takes a dict of configurations and adds it to the widget
        for config in configDict.keys():
            self._widget[config] = configDict[config]
        return self                                        
    
    def execute(self, fill, ipadx, ipady, side, expand):  # Adds widget to root window
        self._widget.pack(fill = fill,
                          ipadx = ipadx,
                          ipady = ipady,
                          side = side,
                          expand = expand)
        return self
    
    def getWidget(self):                                  # Getter for widget
        return self._widget
