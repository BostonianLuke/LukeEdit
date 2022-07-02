# This class is incharge of getting computer information, like monitor resolution and username

import subprocess
from screeninfo import get_monitors

class System:
    
    # Constructor for System that establishs username, screen resoltuin, and the screen's physical dimensions
    def __init__(self):                                                                                             
        self.__userName = subprocess.check_output(["echo","%username%"], shell=True).decode().replace('\r\n','')   # Find username via CMD (used for PATH)
        self.__screenResolution = [[monitor.width, monitor.height] for monitor in get_monitors()]                  # Find screen resolution for centering windows
        self.__screenSize = [[monitor.width_mm, monitor.height_mm] for monitor in get_monitors()]                  # Get screen physical size 
        
    def getUserName(self):              # Getter for username
        return self.__userName              # return username
    
    def getScreenResolution(self):      # Getter for screen resolution
        return self.__screenResolution      # return the primary screen's resolution
    
    def getScreenSize(self):            # Getter for screen's physical size
        return self.__screenSize            # return screen's physical size