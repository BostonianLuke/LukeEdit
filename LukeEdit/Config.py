# This class is incharge of interacting with the user preset file called config.json saved in C:\Users\(USERNAME)\AppData\Local\LukeEdit

from os.path import exists
import os
import json
from System import System

class Config:
    
    def __init__(self):
        self.__userName = System().getUserName()                                               # Find the user's current username
        
        # This will be the default config, if config.json doesn't already exist
        self.__defaultConfig = {"Orientation" : "L",                                           # Orientation of PDF (either 
                                "Vertical" : 25.4,                                             # Margins on the vertical axis
                                "Horizontal" : 25.4,                                           # Margins on the Horizontal axis
                                "OpenLocation" : rf"C:\Users\{self.__userName}\Downloads",     # Default location for opening files
                                "SaveLocation" : rf"C:\Users\{self.__userName}\Documents",     # Default location for saving files
                                "FontSize" : 12}
        
        self.__rootFolder = rf"C:\Users\{self.__userName}\AppData\Local\LukeEdit"              # Root level directory
        self.__configFile = f"{self.__rootFolder}\config.json"                                 # config.json full path
        self.__config = {}                                                                     # raw config data
        self.__checkForConfig()                                                                # Run this to see if a config already exists
        
    def __repr__(self):                                                # Overwrites toString (Java Equivalent) and returns config in stirng form
        return str(self.__config)
    
    def setConfigFile(self):                                           # Write the raw config to the config.json file
        with open(self.__configFile, "w") as file:
            json.dump(self.__config, file)
        return self
        
    def __checkForConfig(self):                                        # This functions checks to see if root directory and config.json 
        if exists(self.__rootFolder) == False:                             # If root doesn't exist
            os.mkdir(self.__rootFolder)                                        # Make root directory
                
            if exists(self.__configFile) == False:                             # If config.json doesn't exist
                self.__config = self.__defaultConfig                               # Set raw config to the default config
                self.setConfigFile()                                               # Create config.json and write to it
        else:
            self.setConfigFromFile()                                       # Else set raw config from config.json
                    
    def __conversionFactor(self, config, factor):                       # Uses to convert margins between millimeters to inches
        for key in config.keys():                                           # For each config
            if key in ["Vertical", "Horizontal"]:                                # If config is a type of margin
                config[key] = round(float(config[key]) * factor,2)                   # Convert margin to either mm: (factor = 25.4) or in: (1 / 25.4) or no change: (factor = 1)
        return config
    
    def getConfig(self):
        return self.__conversionFactor(self.__config, 1)                # Return config, with margins not converted
    
    def setConfig(self, config):                                        # Set raw config to config that is coverted to mm
        self.__config = self.__conversionFactor(config, 25.4)
        return self
                  
    def getConfigFromFile(self):                                        # set raw config from config.json
        with open(self.__configFile) as file:
            config = json.load(file)
        return self.__conversionFactor(config, 1 / 25.4)                # covert the config margins to inches before returning
                    
    def setConfigFromFile(self):                                        # Set raw config based off of config.json
        with open(self.__configFile) as file:
            self.__config = json.load(file)
        return self


