# This class is incharge of the displaying the configuartions for PDF generations and intiating the process of generating a new PDF

import tkinter as tk
from PIL import ImageTk, Image
import datetime
from Config import Config
from System import System
from Root import Root
from Label import Label
from Button import Button
from RadioButtonGroup import RadioButtonGroup
from Spinbox import Spinbox
from FileDialog import FileDialog
from TextDocument import TextDocument
import threading
from PDF import PDF
import os

class ConfigGUI:
    
    def __init__(self, height, width, parent, content, angle = 0):
        self.__height = height                                                      # Height of window
        self.__width = width                                                        # Width of window
        self.__parent = parent                                                      # Main root window (this window will have to be a child of main root)
        self.__content = content                                                    # Final Text document (to print to PDF)
        self.__angle = angle                                                        # Current angle of spining LukeEdit logo
        
        # Configuartions for all radio buttons
        self.__radioButonConfig = {"font" : ("Arial", 15, 'bold'),                                  # Font family, size, and style
                                   "indicator" : 0,                                                 # Dont show radiobutton icon
                                   "background" : "#B63A00",                                        # bg color
                                   "activebackground" : "light blue",                               # Color when you click button
                                   "compound" : tk.TOP,                                             # Image is on top of text
                                   "selectcolor" : "#0F9724"}                                       # Color of button when selected

        # Configuartions for all spinboxes
        self.__spinboxConfig = {"buttonbackground" : "#F0B408",                                     # button bg color
                                "bg" : "#6B6B6B",                                                   # bg color 
                                "from_" : 0,                                                        # First option
                                "to" : 10,                                                          # Last option
                                "increment" : 0.1,                                                  # Increment for options
                                "justify" : tk.CENTER,                                              # Center text that is displayed
                                "wrap" : True,                                                      # If you go past 0, it goes straight to the max
                                "font" : ('Arial',15,'bold')}                                       # Font family, size, and style

        self.__orientationOptions = {"Portrait" : "P", "Landscape" : "L"}                           # orientation options for radio button
        
        self.__previousConfig = Config().setConfigFromFile().getConfigFromFile()                    # Get config from config.json

        screenResolution = System().getScreenResolution()[0]                                        # Get screen resolution
        
        x = (screenResolution[0] // 2) - (self.__width // 2)                                        # starting x of window
        y = (screenResolution[1] // 2) - (self.__height // 2)                                       # starting y of window

        # Root of window (not main root)
        self.__root = Root("child").config(title = "PDF Configuration",                             # Title of window             
                                           state = tk.NORMAL,                                       # Allow users to affect window
                                           geometry = f"{self.__width}x{self.__height}+{x}+{y}",    # Shape and location of window
                                           ico = r"images/LukeEdit.ico",                            # Change icon
                                           resizable = True).topmost(1).topmost(0).getRoot()        # Aloow window to be resizable

        self.__marignPhotos = {direction : ImageTk.PhotoImage(file = f"images/{direction}.png")     # Create dict to hold photos for margins
                               for direction 
                               in ["Vertical", "Horizontal"]}
        
        self.__config = {}                                                                          # Dict for config data
        
    # Create title portion of window
    def title(self, title):
        Label(self.__root).config({"bg" : "#005595",                                                # bg color
                                   "text" : title,                                                  # text for label
                                   "font" : ("Arial", 25, "bold")}).execute(fill = tk.BOTH,         # set font and add label to window
                                                                            ipadx = 0,
                                                                            ipady = 10,
                                                                            side = tk.TOP,
                                                                            expand = True)
        return self
    
    # Create radio button portion of window for PDF orientation
    def orientation(self):
        orientationFrame = tk.Frame(self.__root, bg = "black")                                                 # Create frame object for orientation radio button portion
        orientationPhotos = {key : f"images/{key}.png" for (key, value) in self.__orientationOptions.items()}  # Dict to hold images

        self.__config["Orientation"] = RadioButtonGroup(root = orientationFrame,                               # Assign root to frame (which is assigned to window)
                                                        options = self.__orientationOptions,                   # This is the key : valur for the radio button
                                                        radioButonConfig = self.__radioButonConfig,            # Use radiobutton configs, defined above
                                                        default = self.__previousConfig["Orientation"],        # From previous config, assign default orientation value
                                                        name = "Orientation",                                  # Name of variable for value
                                                        parameterName = "variable").execute(fill = tk.BOTH,
                                                                                            ipadx = 0,
                                                                                            ipady = 10,
                                                                                            side = tk.RIGHT,
                                                                                            expand = True)
        
        orientationFrame.pack(fill = tk.BOTH, side = tk.RIGHT)                                                 # Add the frame to the window
        return self
        
    # Create spinbox portion of window for PDF margins
    def margin(self, direction):
        marginFrame = tk.Frame(self.__root, bg = "black")                                                     # Create frame object for spinbox margins and it's label portion                        

        Label(marginFrame).config({"bg" : "white",                                                            # bg color
                                   "compound" : tk.TOP,                                                       # Have image shown above text
                                   "image" : self.__marignPhotos[direction],                                  # Get images from image dict
                                   "text" : f"{direction} Margin (in):",                                      # text for label
                                   "font" : ("Arial", 15, "bold")}).execute(fill = tk.BOTH,
                                                                            ipadx = 0,
                                                                            ipady = 10,
                                                                            side = tk.TOP,
                                                                            expand = True)

        self.__config[direction] = Spinbox(root = marginFrame,                                                # Assign root to frame (which is assigned to window)                                                        
                                           spinboxConfig = self.__spinboxConfig,                              # Use spinbox configs, defined above
                                           default = self.__previousConfig[direction],                        # From previous config, assign default margins value
                                           name = direction,                                                  # Name varible based on the type of margin
                                           parameterName = "textvariable").config(self.__spinboxConfig).execute(fill = tk.BOTH,
                                                                                                                ipadx = 0, 
                                                                                                                ipady = 5, 
                                                                                                                side = tk.TOP,
                                                                                                                expand = True)
        
        marginFrame.pack(fill = tk.BOTH, side = tk.RIGHT)                                                    # Add the frame to the window
        return self
    
    # Creates button for starting PDF generation
    def createPDF(self):
        Button(self.__root).config({"bg" : "#E7C000",                                                        # bg color                                     
                                    "text" : "Create PDF",                                                   # Text for button
                                    "command" : self.__runFile,                                              # When button is pressed, start PDF generation process
                                    "font" : ("Arial", 15, 'bold')}).execute(fill = tk.BOTH,
                                                                             ipadx = 0,
                                                                             ipady = 0,
                                                                             side = tk.BOTTOM,
                                                                             expand = True)
        return self
    
    # Writes to config file
    def __getConfig(self):
        
        # For each previous conifg, update 
        for key in self.__config.keys():
            self.__previousConfig[key] = self.__config[key].getValue()   # Assign value to Config object
        Config().setConfig(self.__previousConfig).setConfigFile()        # Write config json to config.json
    
    # Destroy main window and get config
    def __destroy(self):
        self.__getConfig()    # Get the current config for PDF generation
        self.__root.destroy() # Destroy root window
    
    # Starts PDF Process
    def __runFile(self):
        self.__destroy()      # Destroy options window
        self.__saveFile()     # Continue PDF generation process
        
    # Spin the LukeEdit logo
    def __changePhoto(self, label, angleChange):
        self.__angle += angleChange                           # Based on the increment, increase angle
        with Image.open("images/LukeEdit.png") as photo:      # While image is open:
            photo = photo.resize((150, 150))                      # Make image smaller
            photo = photo.rotate(self.__angle)                    # rotate image based off of new angle
        image = ImageTk.PhotoImage(photo)                     # Convert image to ImageTk 
        label.config({"image" : image})                       # Add image to label's config dict
        label.getWidget().image = image                       # Add image to progress window
        
    # Check to see if thread (PDF is still being generated) is still active
    def __isAlive(self, thread, root, label, path, start):
        
        # Provide a msg with duration of process
        label.config({"text" : 
                      f"PDF is being generated\nDuration:  {(datetime.datetime(2000, 1, 1) + (datetime.datetime.now() - start)).strftime('%H:%M:%S')}"})  
        
        # Rotate LukeEdit logo
        angle = self.__changePhoto(label, angleChange = -45)
        
        # If PDF is done generating (thread is dead), destroy window and open PDF
        if not thread.is_alive():
            root.destroy()          # Destroy window
            os.startfile(path)      # Open PDF
        else:
            # Circular reference of this method (start process over again)
            root.after(500, lambda: self.__isAlive(thread, root, label, path, start))
            
    # This creates the progress window, while PDF is being generating
    def __waitingMessage(self, angle, thread, path):
        width = 600                                                                        # Width of window
        height = 200                                                                       # Height of window
        screenResolution = System().getScreenResolution()[0]                               # Get screen resolution
        x = (screenResolution[0] // 2) - (width // 2)                                      # Calculate x (center)
        y = (screenResolution[1] // 2) - (height // 2)                                     # Calculate y (center)

        # Create root for the progress window
        root = Root("parent").config(title = "Test",                                       # Title will not be used (this window will not have top bar
                                     state = tk.NORMAL,                                    # Allow people to interact with window
                                     geometry = f"{width}x{height}+{x}+{y}",               # Controls shape and location of window
                                     ico = r"images/LukeEdit.ico",                         # ico will not be used, window will not have top bar
                                     resizable = True).topmost(1).topmost(0).getRoot()     # Allow window to be resizable 

        root.overrideredirect(1)                                                           # This will eliminate top bar of window
        
        with Image.open("images/LukeEdit.png") as photo:                                   # While image is open:
            photo = photo.resize((150, 150))                                                   # Make image smaller
            photo = photo.rotate(angle)                                                        # rotate image based off of new angle
        image = ImageTk.PhotoImage(photo)                                                  # Convert image to ImageTk 

        # initial label, before progress has been made (lacks duration)
        label = Label(root).config({"text" : "PDF is being generated   ",                  # msg minus duration
                                    "image" : image,                                       # Add image
                                    "font" : ("Arial", 25, "bold"),                        # Control font
                                    "anchor" : tk.CENTER,                                  # Center this label's text
                                    "compound" : tk.RIGHT}).execute(fill = tk.BOTH,        # Make image appear to the right of text
                                                                    ipadx = 0,
                                                                    ipady = 0,
                                                                    side = tk.TOP,
                                                                    expand = True)

        start = datetime.datetime.now()                                                    # This is whent he process started                                           
        root.after(500, lambda: self.__isAlive(thread, root, label, path, start))          # Initial isAlive method use, after this, the method is used via circular
        root.mainloop()                                                                    # Create the progress window
        
    def __saveFile(self):
        filePath = FileDialog().getSaveFilePath(title = "Save", fileTypes = [("pdf file", "*.pdf")])    # Ask for filepath of new PDF
        if filePath:                                                                                    # If filepath is provided:
            document = TextDocument(filePath = filePath, content = self.__content)                          # Create a new TextDocument object with string provided by user
            self.__parent.destroy()                                                                         # Destroy the main GUI application
            angle = 0                                                                                       # Initial angle for LukeEdit logo for progress window
            config = Config().setConfigFromFile()                                                           # Config form PDF, the user chose
            thread = threading.Thread(target = PDF(document, config).createOptimalPDF)                      # Create a thread, dedicated to generating an optimal PDF
            thread.start()                                                                                  # Start this thread
            self.__waitingMessage(angle, thread, filePath)                                                  # Initiate the waiting message (that is defined above)
        
    # Create the main window and bind some commands
    def execute(self):                  
        self.__root.focus_force()                                           # Focus user on this window
        self.__root.protocol("WM_DELETE_WINDOW", self.__runFile)            # If window is destroy via X at the top, run PDF Generation
        self.__root.bind("<Control-Key-p>",lambda event: self.__runFile())  # Bind Ctrl P to run PDF Generation
        self.__root.mainloop()                                              # Create the main window
        
        return self