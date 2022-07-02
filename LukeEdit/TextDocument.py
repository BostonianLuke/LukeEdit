# This class is incharge of interacting with a string based word document 

from tkinter import messagebox
from System import System
from FileDialog import FileDialog

class TextDocument:
    
    # TextDocument's constructor
    def __init__(self, filePath = "", content = []):
        self.__filePath = filePath                                         # This will be the path of the orignal text document or the new location
        if type(content) == str:                                           # If content is a string datatype:                          
            self.__content = content.split('\n')                               # Convert string to list, split by special chatacter \n (new line char)
            self.__stringOriginally = True                                     # set stringOriginally to True (When object was created, it's content was inially string)
        else:                                                              # Else:
            self.__content = content                                           # Content does not need to be modified 
            self.__stringOriginally = False                                    # set stringOriginally to False (When object was created, it's content was inially list)
        self.__userName = System().getUserName()                           # Find the user's username for path creation
        
    # This override the toString method (Java equiv)
    def __repr__(self):
        return ''.join(self.__content[:50])                                # Show first 50 lines of document
    
    # This function will be used to open a text document and setContent (mehthod)
    def openFile(self):
        self.__filePath = FileDialog().getOpenFilePath(title = "Open")     # Get filepath of content                                 
        if self.__filePath:                                                # If file is chosen
            with open(self.__filePath) as file:                                # while file is open
                try:                                                               # Try to read from file
                    self.__content = file.readlines()                                  # If successful, add contetn from file to content variable
                except UnicodeDecodeError:                                         # If UnicodeDecodeError, provide custom error message (file type not suppored by LukeEdit)
                    self.__filePath = ""                                               # make file path empty
                    
                    # Returm custom error message
                    messagebox.showerror('File Type Error', 'LukeEdit does not support this file type')
                    
        return self
    
    # Get content in either string or list format
    def getContent(self):
        if self.__stringOriginally:
            return '\n'.join(self.__content)                           # If stirng originally join the list by the special character (creating single giant string)
        else:
            return ''.join(self.__content)                             # If not a string (when object was created), there are no special characters "\n" so you join on black ""

    # Find how many lines are in the text document
    def getLength(self):
        return len(self.__content)
    
    # Find the max number of chars per line (for the entire document)
    def getMaxChar(self):
        return max([len(line) for line in self.__content])
    
    # Return the last part of the filepath (the file's name)
    def getFileName(self):
        return self.__filePath.split("/")[-1]
    
    # Return full file path (associated with the text document)
    def getFilePath(self):
        return self.__filePath
    
    # Return the raw content (in the form of a list of strings (which represent each line of the document))
    def getContentList(self):
        return self.__content
    
    # This will return the index of the line (where the specific case insensitive target was found
    def findTarget(self, target):
        if target:                                                    # If target is not an empty string
            i = 0                                                     # var to hold current index (line)
            linesFound = []                                           # Hold all lines, where target is found                    
            for line in [line.lower() for line in self.__content]:    # For each line in a lower case form of the raw document
                if line.find(target.lower()) != -1:                       # If lower case target is found in lower case line
                    linesFound.append(i)                                      # Add the line index to the final list
                i += 1                                                    # Move on to next line

            return linesFound                                         # Return the find list 

