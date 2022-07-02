# Child of widget, wrapper class for Tkinter's scrolledtext class and 

import tkinter.scrolledtext as scrolledtext
from Widget import Widget
from Config import Config
import tkinter as tk

class Text(Widget):
    
    def __init__(self, root, document):                                           
        self.__document = document                                                   # document will be text to display in widget
        self._widget = scrolledtext.ScrolledText(root)                               # Assigns widget var to tkinter's ScrolledText widget from tkinters scrolledtext
        self._widget.insert("1.0", self.__document.getContent())                     # Add document to the widget
        self.__previousConfig = Config().setConfigFromFile().getConfigFromFile()     # Read config.json (which creates a dict file in memory, with the presets the program uses)
        self.config({"font" : ("Courier", self.__previousConfig["FontSize"])})       # Font size will be initially be based on config.json
        self._widget.tag_configure("center", justify = "center")                     # Create tag that will center the text displayed
        self._widget.tag_add("center", "1.0", "end")                                 # Add this tag to widget
        self.__selectedPoints = []                                                   # Hold coords of the first and last line selected
        self.__savedQuery = []                                                       # Holds lines where target query was found in widget
        self.__curentIndex = -1                                                       # Current line selected
    
    def highlightLine(self):                                                      # Method to highlight a specfic line
        if self._widget.tag_ranges("highlight"):                                     # If Line is already highlighted:                 
            self._widget.tag_delete("highlight")                                        # Remove highlight tag
        index = int(float(self._widget.index(tk.CURRENT)))                           # Get current line selected 
        self._widget.tag_configure("highlight",background = "#004145")               # Create highlight tag
        self._widget.tag_add("highlight", f"{index}.0", f"{index + 1}.0")            # Add highlight tag
        
    def makeSelection(self):                                                       # Based on where the user's mouse is, will make a selection of the first and last line of txt doc                                                  
        index = int(float(self._widget.index(tk.INSERT)))                             # Index of current mouse location 

        # If there is no current slection or if there is a current selection and the current mose location is diffrent from the last selection 
        if (len(self.__selectedPoints) == 0) or ((len(self.__selectedPoints) > 0) and (f"{index}.0" != self.__selectedPoints[-1][0])):    

            # Only two lines (beginning and end) can be selected. if it's a thrid point, the current selection resets
            if len(self.__selectedPoints) % 2 == 0:
                self._widget.tag_delete("selection")                              # Stop highlighting current lines that are selected
                self._widget.tag_delete("select")                                 # Stop highlighting current line selected

            self._widget.tag_configure("select",background="#97910F")             # Define the line selection color
            self._widget.tag_add("select", f"{index}.0", f"{index + 1}.0")        # Highlight selected line
            
            self.__selectedPoints.append((f"{index}.0", f"{index + 1}.0"))        # Add the the selection to a list
            
            if len(self.__selectedPoints) % 2 == 0:                               # If two lines are selected"
                self._widget.tag_configure("selection",background = "#97910F")        # Define the color for multiple line selection
                
                # If the first selected line is less than the current selected line (Forward)
                if index > int(float(self.__selectedPoints[-2][0])):                                          
                    self._widget.tag_add("selection", self.__selectedPoints[-2][0], self.__selectedPoints[-1][1])

                # If the first selected line is greater than or equal to the current selected line (Backward)
                else:
                    self._widget.tag_add("selection", self.__selectedPoints[-1][0], self.__selectedPoints[-2][1])
                     
    def __updateCurrentIndex(self, direction):                                          #Finds the desired word location and highlights it
        
        # If a word has already been found, reset the selection 
        if self._widget.tag_ranges("find"):
            self._widget.tag_remove("find", "1.0", "end")                                   #Remove highlighting of specfic word found
            
        self._widget.tag_configure("find", background = "#646464", foreground = "black")    # Define the highlight style for word found
        self.__curentIndex = ((self.__curentIndex + direction) % len(self.__savedQuery))    # Current selected word found (ex. 3 of 30 for "Hello Wolrd")
        self._widget.tag_add("find",                                                        # Name of tag
                             f"{self.__savedQuery[self.__curentIndex]}.0",                  # Begining index of word found
                             f"{self.__savedQuery[self.__curentIndex] + 1}.0")              # Ending index of word found
        self._widget.see(f"{self.__savedQuery[self.__curentIndex]}.0")                      # Focus user perspective on word found
        return f"{self.__curentIndex+1} of {len(self.__savedQuery)}"                        # Return the location of this word, in relation to all items found (ex. 3 of 30)
    
    def queryFile(self, target, direction):                                                 # This queries the text widget for desired word                                   
        self._widget.focus_force()                                                               # Focus user perspective on input
        if self.__savedQuery:                                                                    # If a word has been found or a query has already been made to the TextDocument object
            return self.__updateCurrentIndex(direction)                                              # Find the word location and highlight
        else:                                            
            self.__savedQuery = [index + 1 for index in self.__document.findTarget(target)] # If query has not already been made to the TextDocument object, do it using findTarget method
            
            if self.__savedQuery:                            # If word is found
                return self.__updateCurrentIndex(direction)       # Find the word location and highlight
            else:
                return "Not Found"                           # Word has not been found
            
    def resetSelectedPoints(self):              # Resets all tags related to class
        self.__selectedPoints = []                    # Reset list that holds selected points
        self.__savedQuery = []                        # Reset list that holds the locationms of a specific word found
        self.__curentIndex = -1                        # Reset the var that hold whihc line is currently selected
        self._widget.tag_delete("selection")          # Reset the tag for multiples lines selected
        self._widget.tag_delete("select")             # Reset the tag for a single line selected