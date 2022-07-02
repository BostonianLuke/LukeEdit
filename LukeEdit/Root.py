#Creates a GUI window

import tkinter as tk

class Root:
    
    def __init__(self, rootType):
        if rootType == "parent":                               # Indicates if window is the main windows of an application
            self.__root = tk.Tk()                                  # If it is: using tkinter's TK() method 
        else:
            self.__root = tk.Toplevel()                            # Else: use tkinters Toplevel() method
            
    def config(self, title, geometry, ico, state, resizable):  # Used for setting up window configurations
        self.__root.geometry(geometry)                             # Size and position of window
        self.__root.iconbitmap(ico)                                # Add custom icon for window
        self.__root.state(state)                                   # This makes the window fullscreen (except for Winodws taskbar)
        self.__root.title(title)                                   # Title for window
        self.__root.resizable(resizable, resizable)                # Control if the window can be resizable
        return self
    
    def topmost(self, topmostValue):                           # Make window either topmost or not topmost
        self.__root.attributes("-topmost", topmostValue)
        return self                                                     
    
    def hide(self):                                            # Hide window
        self.__root.withdraw()
        return self                                        
    
    def show(self):                                            # Show window
        self.__root.deiconify()
        return self                                         
        
    def getRoot(self):                                         # Getter for root window
        return self.__root
    
    def execute(self):                                         # Run window loop
        self.__root.mainloop()