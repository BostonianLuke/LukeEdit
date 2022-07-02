# This class is a wrapper for tkinter's Menu object

import tkinter as tk

class Menu:
    
    # Constructor 
    def __init__(self, root):
        self.__menuBar = tk.Menu(root)                                                            # This is the entire menu object                                          
        self.__menuTabs = {}                                                                      # This dict will hold allt he tabs, within the menu (File, Edit, etc.)
        root.config(menu = self.__menuBar)                                                        # Add the menu object to the main root window

    # Attach tabs to menu object
    def addTab(self, *tabs):
        for tab in tabs:                                                                          # For each tab in the tab's list
            self.__menuTabs[tab] = tk.Menu(self.__menuBar, tearoff = 0)                                # Add a menu object to the tab dict
            self.__menuBar.add_cascade(label = tab, menu = self.__menuTabs[tab], underline = 0)        # Add the menu object, to the parent menu object
        return self
    
    # Assign a tab a specifc command and label (like Save)
    def addCommand(self, tab, label, config, command = None):
        if command:                                             # If command is not None
            config["command"] = command                             # Assign a command to a label
        config["label"] = label                                 # Assign a label to the command
        self.__menuTabs[tab].add_command(config)                # Add this command to the tab
        return self