# LukeEdit application

from TextDocument import TextDocument
from Root import Root
import tkinter as tk
from Menu import Menu
from Label import Label
from Entry import Entry
from PIL import ImageTk, Image
from Text import Text
from Justify import Justify
from Controller import Controller
from FileDialog import FileDialog

def main():
    document = TextDocument().openFile()                                                                     # Ask the user to find a new file and then open it and get content              
    if document.getFilePath():                                                                               # If user selects a file:
        rootObject = Root("parent").hide()                                                                       # Create a root object for the main window and hide it
        root = rootObject.getRoot()                                                                              # Assign Tkinter's root object to root var
        
        # This will hold the configs for the text widget 
        textConfig = {"fg" : "white",                                                                            # fg color                                                                    
                      "bg" : "black",                                                                            # bg color
                      "height" : document.getLength(),                                                           # determine the height of text widget by finding num of lines
                      "width" : document.getMaxChar(),                                                           # determine the width of text widget by finding max char per line
                      "cursor" : "dotbox",                                                                       # change cursor to the default for view mode
                      "state" : tk.DISABLED,                                                                     # change state to default for view mode
                      "selectbackground" : "black",                                                              # vide mode requires a select bg of black
                      "padx" : 0,                                                                                # padding of x axis
                      "pady" : 0,                                                                                # padding of y axis
                      "undo" : True}                                                                             # Aloow the user to ctrl z, when they make mistake
        
        # config for interactive menu bar
        menuButtonConfig = {"state" : tk.NORMAL,                                                                 # Make it so user can interact with it                                   
                            "font" : ("Courier", 8)}                                                             # Font style
        
        # config for non-interactive menu bar
        menuLabelConfig = {"state" : tk.DISABLED,                                                                # Make it so user cannot interact with it    
                           "font" : ("Courier", 8)}                                                              # Font style
            
        menu = Menu(root).addTab("File", "Edit", "Settings")                                                     # These will be the tabs for menu
        
        findFrame = tk.Frame(root)                                                                               # Frame for widgets that are displayed above Tkinters Text widget
        
        # Used to display the count of words found 
        findCountLabel = Label(findFrame).config({"text" : "",                                                   # Since nothing was found yet, default to blank string
                                                  "font" : ("Arial", 12, "bold")}).execute(fill = tk.BOTH,       
                                                                                           ipadx = 5,
                                                                                           ipady = 0,
                                                                                           side = tk.LEFT,
                                                                                           expand = True)
        
         # Used to allow user to enter a word, that they want to find
        entry = Entry(findFrame).config({"font" : ("Arial", 15)}).execute(fill = tk.Y,
                                                                          ipadx = 0,
                                                                          ipady = 0,
                                                                          side = tk.LEFT,
                                                                          expand = False)
        # Open the magnifying glass symbol and resize it
        with Image.open("images/zoom.png") as photo:
            photo = photo.resize((25, 25))
            
        image = ImageTk.PhotoImage(photo)                                                                       # Convert the symbol to Tkinter's ImagerTk file
        
        fontSizeLabel = Label(findFrame).config({"text" : "",                                                   # Used to display the current font size of text within the text widget, blank first
                                                 "font" : ("Arial", 12, "bold"),                                # Font of label
                                                 "image" : image,                                               # Show magnifying glass symbol to the left (closer to the entry object)
                                                 "compound" : tk.LEFT}).execute(fill = tk.BOTH,
                                                                                 ipadx = 0,
                                                                                 ipady = 0,
                                                                                 side = tk.LEFT,
                                                                                 expand = True)
        # This will show which mode Luke Edit is in
        modeLabel = Label(findFrame).config({"text" : "",
                                             "font" : ("Arial", 12, "bold")}).execute(fill = tk.BOTH,
                                                                                      ipadx = 10,
                                                                                      ipady = 0,
                                                                                      side = tk.LEFT,
                                                                                      expand = True)
        
         # Add all these items to the main window
        findFrame.pack(side = tk.TOP) 
        
        # Add the text widget to the main window (below all the other stuff)
        text = Text(root, document = document).config(textConfig).execute(fill = tk.BOTH,
                                                                          ipadx = 0,
                                                                          ipady = 0,
                                                                          side = tk.TOP,
                                                                          expand = True)
        
         # Add a radio group that allows the user to moddify the justify of the text
        Justify(root = findFrame, textWidget = text.getWidget())

 
        
        
        
        # Create the controller class with all the user interactive functionality
        controller = Controller(rootObject = rootObject, 
                                text = text, 
                                entry = entry, 
                                findCountLabel = findCountLabel, 
                                fontSizeLabel = fontSizeLabel, 
                                modeLabel = modeLabel)
        
        # All the menu options (which are self explaintory) and I'm too lazy to continue commenting
        menu.addCommand("File", "New File", menuButtonConfig, lambda: controller.newFile(root, main))
        
        menu.addCommand("Edit", "Create PDF                       Ctrl+P", menuLabelConfig)
        menu.addCommand("Edit", "Save File                        Ctrl+S", menuLabelConfig)
        menu.addCommand("Edit", "Increase Font Size            Ctrl+Plus", menuLabelConfig)
        menu.addCommand("Edit", "Decrease Font Size           Ctrl+Minus", menuLabelConfig)
        menu.addCommand("Edit", "Query Text Down             Right Arrow", menuLabelConfig)
        menu.addCommand("Edit", "Query Text Down                   Enter", menuLabelConfig)
        menu.addCommand("Edit", "Query Text Up                Left Arrow", menuLabelConfig)
        menu.addCommand("Edit", "Line Selection        Left Mouse Button", menuLabelConfig)
        menu.addCommand("Edit", "Reset Selection      Right Mouse Button", menuLabelConfig)
        menu.addCommand("Edit", "Reset Selection                  Ctrl+Z", menuLabelConfig)
            
        menu.addCommand("Settings", "Save Location", menuButtonConfig, lambda: FileDialog().getFolderPath(label = "SaveLocation"))
        menu.addCommand("Settings", "Open Location", menuButtonConfig, lambda: FileDialog().getFolderPath(label = "OpenLocation"))  
        
        # Show the root object finally 
        rootObject.show().config(title = document.getFileName(),          # Title is determined by the orignal file's name 
                                 geometry = "",                           # Geometry is not required due to zoomed state
                                 ico = r"images/LukeEdit.ico",            # Add the custom LukeEdit logo
                                 state = "zoomed",                        # Makes the application fullscreen except for the Windows 10 toolbar
                                 resizable = True).topmost(1).topmost(0)  # Allow the main window to be reizable and makeit the top most window for a second
        
        root.mainloop()                                                   # Run the main window of LukeEdit
test = main()                                                             # Execute LukeEdit application
print("DONE")

