# This class creates a PDF and gathers information on a PDF document

import fpdf
import pdfplumber

class PDF:
    
    # Constructor
    def __init__(self, document, config):
        self.__document = document                                                 # Raw String, that will be added to PDF
        self.__filePath = document.getFilePath()                                   # Save location for PDF
        self.__config = config                                                     # Config object that contains settings for PDF document like (margins, orientation, etc.)
 
    # Create FPDF object and gettting the configs from the Config object
    def __configPDF(self):
        pdf = fpdf.FPDF(format = 'letter', 
                        orientation = self.__config.getConfig()["Orientation"])      # Create FPDF and assign orientation
        
        pdf.set_margins(left = self.__config.getConfig()["Horizontal"],              # Assign left (Horizontal Marign)
                        top = self.__config.getConfig()["Vertical"])                 # Assign right (Vertical Marign)
        
        pdf.set_auto_page_break(auto = True,                                         # Auto page break on
                                margin = self.__config.getConfig()["Vertical"])      # Assign bottom (Vertical Marign)                                
        pdf.add_page()                                                               # Create a new page for PDF (Required before creating a PDF)
        return pdf                                                                   # Return FPDF object

    # Create the PDF document
    def __createPdf(self, fontSize, text):
        pdf = self.__configPDF()                       # Configure PDF document
        pdf.set_font("Courier", size = fontSize)       # Set font and font size
        pdf.multi_cell(w = 0, h = 5, txt = text)       # Add text to PDF document
        pdf.output(self.__filePath)                    # Create and save PDF document

    # Find the number of characters, on the first line of the first page of the PDF ducment created
    def __getCharLenPDF(self):
        with pdfplumber.open(self.__filePath) as pdfFile:                 # While PDF document is opened
            return len(pdfFile.pages[0].extract_text().split('\n')[0])        # From the first page, convert string to list and get first line's length

    # Find the optimal font size, for the PDF document
    def createOptimalPDF(self):
        maxChar = self.__document.getMaxChar()                                          # Find the max chars per line of raw text document
        increment = 0.1                                                                 # Each iter of the algorithm will be incremented by this number
        fontSize = increment                                                            # This will be the smallest font size used
        while True:                                                                     # Run algorithm loop until optimal font size is found
            self.__createPdf(fontSize, "O" * maxChar)                                       # Create a test PDF with just "O"'s
            currentCharLen = self.__getCharLenPDF()                                         # Then find out if this fontsize caused the line to break
            
            if currentCharLen < maxChar:                                                    # If the line broke
                self.__createPdf(fontSize - increment, self.__document.getContent())             # Create the actual final PDF, with raw text and the optimal font size
                break                                                                            # Break out of the loop
                
            fontSize += increment                                                           # Go to the next font size to test
