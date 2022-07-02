# This class is incharge of all the commands and keybinding (the user is allowed to do)

from Config import Config
import tkinter as tk
from ConfigGUI import ConfigGUI
from System import System

class Controller:
    
    # Constructor
    def __init__(self, rootObject, text, entry, findCountLabel, fontSizeLabel, modeLabel):
        self.__rootObject = rootObject                                                        # This is the main application window class object
        self.__root = self.__rootObject.getRoot()                                             # This is the main application window                              
        self.__text = text                                                                    # This is the wrapper class object for tkinter's textscolled wdiget
        self.__entry = entry                                                                  # This is the wrapper class object for tkinter's Entry wdiget
        self.__findCountLabel = findCountLabel                                                # This label will either display nothing, the number of results found, or an error message
        self.__fontSizeLabel = fontSizeLabel                                                  # This will show the font size of the text information displayed in the Text widget
        self.__modeLabel = modeLabel                                                          # This will display either View Mode or Edit Mode
        self.__currentConfig = Config().setConfigFromFile().getConfigFromFile()               # Read config from config.json
        self.__fontSizeLabel.config({"text" : f"{self.__currentConfig['FontSize']} pts"})     # Initialize font size based on config.json
        self.__viewMode()                                                                     # Set application to view mode by default
        
    # This is the settings and keybindings for view mode
    def __viewMode(self):
        self.__entry.getWidget().focus_force()                                                     # Focus user cursor on the entry widget for finding queries                                                                                
        self.__modeLabel.config({"text" : "- View Mode"})                                          # Change the mode label to View Mode
        self.__text.config({"cursor" : "dotbox",                                                   # Change cursor symbol to dotbox (Making it easier to select lines)
                            "selectbackground" : "black",                                          # Eliminate the ability for people to highlights parts of lines
                            "state" : tk.DISABLED})                                                # Disbale the user's ability to edit text that is displayed in the Text widget
        self.__root.bind("<Escape>",                 lambda event: self.__root.destroy())          # When user clicks escape, they will destory the Luke Edit Application
        self.__root.bind("<Button-1>",               lambda event: self.__text.makeSelection())    # When a user left clicks, they can select either the first or last line of selection
        self.__entry.getWidget().bind("<Button-1>",  lambda event: self.__resetSelection())        # When a user right clicks on the entry widget, they can reset everything  
        self.__root.bind("<Button-3>",               lambda event: self.__resetSelection())        # When a user right clicks, they can reset everything (Word searched, lines selected)
        self.__root.bind("<Control-Key-z>",          lambda event: self.__resetSelection())        # When a user clicks Ctrl-Z, they can reset everything (Word searched, lines selected)
        self.__root.bind("<Return>",                 lambda event: self.__queryFile(1))            # When a user clicks Enter, start query for word going from top to bottom
        self.__root.bind("<Left>",                   lambda event: self.__queryFile(-1))           # When a user clicks Left Arrow, start query for word going from bottom to top
        self.__root.bind("<Right>",                  lambda event: self.__queryFile(1))            # When a user clicks Right Arrow, start query for word going from top to bottom
        self.__root.bind("<Control-Key-p>",          lambda event: self.__createPDF())             # When a user clicks Ctrl-P, The lines current selected will be used and the PDF creation will cont
        self.__root.bind("<Control-Key-s>",          lambda event: self.__saveFile())              # When a user clicks Ctrl-S, The lines current selected will be saved as a new txt doc
        self.__text.getWidget().bind("<Motion>",     lambda event: self.__text.highlightLine())    # When a user moves mouse, the line where mouse is over will  be highlighted
        self.__root.bind("<Control-minus>",          lambda event, fontSizeDirection = -1: self.__changeFontSize(event, fontSizeDirection)) # Decrease font size of text displayed in text widget
        self.__root.bind("<Control-equal>",          lambda event, fontSizeDirection = 1: self.__changeFontSize(event, fontSizeDirection))  # Decrease font size of text displayed in text widget
        self.__root.bind("<Control-Key-e>",          lambda event: self.__editMode())              # When a user clicks Ctrl-E, go to Edit Mode
        
    # This is the settings and keybindings for edit mode
    def __editMode(self):
        self.__modeLabel.config({"text" : "- Edit Mode"})                           # Change the mode label to Edit Mode                      
        self.__resetSelection()                                                     # Reset to default state
        self.__text.getWidget().focus_force()                                       # Focus user cursor on the entry widget for finding queries      
        self.__entry.getWidget().unbind("<Button-1>")                               # Unbind the ability for a user to reset everything
        self.__text.config({"cursor" : "xterm",                                     # Change cursor to the one most common for text editing
                            "selectbackground" : "lightblue",                       # Chnage the select color
                            "state" : tk.NORMAL,                                    # Enable eiditng of the content within the Text widget
                            "insertbackground" : "white"})                          # change the insert background to white
        self.__root.unbind("<Button-1>")                                            
        self.__root.unbind("<Button-3>")                                            # Unbind the ability for a user to reset everything
        self.__root.unbind("<Control-Key-z>")                                       # Unbind the ability for a user to reset everything
        self.__root.unbind("<Return>")                                              # Unbind the ability for a user to comb through a searched result
        self.__root.unbind("<Left>")                                                # Unbind the ability for a user to comb through a searched result
        self.__root.unbind("<Right>")                                               # Unbind the ability for a user to comb through a searched result
        self.__root.unbind("<Control-Key-p>")                                       # Unbind the ability for a user to create a PDF based off a selection
        self.__root.unbind("<Control-Key-s>")                                       # Unbind the ability for a user to save a file bassed off a slection
        self.__text.getWidget().unbind("<Motion>")                                  # Unbind the auto highlighting caused by mouse movement
        self.__root.bind("<Control-Key-e>", lambda event: self.__viewMode())        # Go back to view mode (allowing for the toggling of modes)

    # This method's sole focus, is reseting LukeEdit back to it's default state
    def __resetSelection(self):
        self.__text.getWidget().tag_delete("selection")                             # Remove any highlighted sections
        self.__text.getWidget().tag_delete("select")                                # Remove any hightlighted lines
        self.__text.getWidget().tag_delete("find")                                  # Remove any highlighted found words
        self.__text.getWidget().tag_delete("highlight")                             # Remove any lines that used the Text object's highlightLine method
        self.__findCountLabel.getWidget().config(text = "")                         # Remove any text within the findCountLabel
        self.__entry.getWidget().delete(0, tk.END)                                  # Remove any text entered within the Enrty widget
        self.__entry.getWidget().focus_force()                                      # Refocus user's cursor back to the Entry widget object
        self.__text.resetSelectedPoints()                                           # Reset any lines that were selected and ready to be converted to txt or pdf
        
    # This method starts the process of find a sopecfic word, that the user entered into the Entry widget
    def __queryFile(self, direction): 
        result = self.__entry.getInput()                         # Get the information the user entered
        if result:                                               # If user did in fact, enter text
            count = self.__text.queryFile(result, direction)          # Utilize the text objects queryFile (which utilizes the TextDocuments's find feature), which has spits out a num of found items
            self.__findCountLabel.config({"text" : count})            # Show to the user, the number of found items, and whihc item is currently highlighted
    
    # This method starts the process of converting a user's selction of lines, into a properly formatted PDF document
    def __createPDF(self):
        # If the user selected muluple lines
        if self.__text.getWidget().tag_ranges("selection"):
            # Get the user's selected lines
            content = self.__text.getWidget().get("selection.first", "selection.last")
            # And give the user the PDF configuration window (so they can choose how the PDF should be formatted)
            ConfigGUI(height = 400, width = 900, parent = self.__root, content = content).title("PDF Configuration").createPDF().orientation().margin("Vertical").margin("Horizontal").execute()
        # If the user did not slelect any lines, provide them a simple error message
        else:
            self.__findCountLabel.config({"text" : "No Lines Selected"})
    # This method saves a user's selction of lines, into a new text document
    def __saveFile(self):
        filePath = FileDialog().getSaveFilePath(title = "Save", fileTypes = [("text file", "*.txt")]) # Ask the user for the location, of this new texdt document
        if filePath:                                                                                  # If the user did in fact chose a location
            content = self.__text.getWidget().get("selection.first","selection.last")                     # Get the user's selected lines
            with open(filePath, 'w') as file:                                                             # While the new empty file is created and open
                file.write(content)                                                                           # Write selected lines to file 
            self.__root.destroy()                                                                         # Destroy LukeEdit application
            os.startfile(filePath)                                                                        # Open new text document
    
    # Increase or decrease the font size of the text displayed in the Text widget 
    def __changeFontSize(self, event, fontSizeDirection):
        previousConfig = Config().setConfigFromFile().getConfigFromFile()                             # Get the configs from the config.json file
        currentFontFamily = self.__text.getWidget().cget('font').split(' ')[0]                        # Find out what the current font is
        currentFontSize = int(self.__text.getWidget().cget('font').split(' ')[-1])                    # Find only what the font size is                     
        newFontSize = currentFontSize + fontSizeDirection                                             # Increase or decrease the current font size
        self.__text.getWidget().config(font = (currentFontFamily, newFontSize))                       # Add the new font size to the Text widget
        #self.__entry.getWidget().config(font = (currentFontFamily, newFontSize))
        previousConfig["FontSize"] = newFontSize
        self.__fontSizeLabel.config({"text" : f"{newFontSize} pts"})                                  # Display what the new font size is 
        Config().setConfig(previousConfig).setConfigFile()                                            # Add this new font size to the config.json
        
    # This uses recursion to create a new instance of LukeEdit
    def newFile(self, root, main):
        self.__root.destroy()                                    # Destroy the current Luke Edit instance
        main()                                                   # Create a new instance of LukeEdit


