# This class is used for using the file dialog menu

import tkinter.filedialog as tk_FileDialog
import tkinter as tk
from Config import Config
from Root import Root

class FileDialog:
    
    def __init__(self):
        self.__previousConfig = Config().setConfigFromFile().getConfigFromFile()                    # This will get previous configs (defualt save and open locations)
    
    # Get open path of file
    def getOpenFilePath(self, title):
        
        #This root object is only used for making the file dialog window the topmost
        rootObject = Root(rootType = "parent").hide().config(title = "Make File Dialog Top Most",   # Not important
                                                      geometry = "",                                # Not important
                                                      ico = r"images/LukeEdit.ico",                 # Not important
                                                      state = tk.NORMAL,                            # Not important
                                                      resizable = False).topmost(1).hide()          # Not important
        
        initialDir = self.__previousConfig["OpenLocation"]                                     # Get the default open location 
        openPath = tk_FileDialog.askopenfilename(initialdir = initialDir,                      # Use the default to set initial opening directory
                                                 title = title)                                # Set title, to let user knowing they are opening a file
        rootObject.show().getRoot().destroy()                                                  # Destroy the root object (not needed anymore)
        return openPath                                                                        # Return either the path or an empty string
    
    # Get path of folder and change the config.json default save or open location
    def getFolderPath(self, label):
        initialDir = self.__previousConfig[label]                                              # Get the default open or save location    
        self.__previousConfig[label] = tk_FileDialog.askdirectory(initialdir = initialDir,     # Use the default to set initial opening or saving  directory
                                                                  title = label[:4])           # title will let user know if they are changing the default open or save location
        if self.__previousConfig[label]:                                                       # If user does select a valid path:
            Config().setConfig(self.__previousConfig).setConfigFile()                               # Change the default open or save location on file in config.json
    
    # Get save path of file
    def getSaveFilePath(self, title, fileTypes):
        initialDir = self.__previousConfig["SaveLocation"]                                     # Get the default save location          
        savePath = tk_FileDialog.asksaveasfilename(default = initialDir,
                                                   initialdir = initialDir,                    # Use the default to set initial saving directory
                                                   title = title,                              # Set title of window "Save"
                                                   filetypes = fileTypes)                      # Set the default file types for saving the file
        return savePath                                                                        # Return the path for the new file or empty string