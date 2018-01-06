class Message () :
    def action(self, braille_gui):
        pass
    
class PrinterMessage(Message) :
    def __init__(self):
        self.message = "printer message"
        
    def action(self, braille_gui):
        print (self.message)

class ReservedPrinter(PrinterMessage):
    def __init__(self):
        self.message = "printing in course..."
    
    def action(self, braille_gui):
        braille_gui.ids.selectOutput.disabled= True
        braille_gui.ids.btnPrinter.disabled= True
        print (self.message)

class ConnectedPrinter(PrinterMessage):
    def __init__(self):
        self.message = "printer connected."
        
    def action(self, braille_gui):
        braille_gui.connectedPrinter= True
        print (self.message)

class UnconnectedPrinter(PrinterMessage):
    def __init__(self):
        self.message = "printer unconnected."
    
    def action(self, braille_gui):
        braille_gui.ConnectedPrinter= False
        print (self.message)

class FreedPrinter(PrinterMessage):
    def __init__(self):
        self.message = "printer freed."
    
    def action(self, braille_gui):
        braille_gui.ids.selectOutput.disabled= False
        braille_gui.ids.btnPrinter.disabled= False
        print (self.message)

class ProgressMessage(PrinterMessage) :
    
    def __init__(self):
        self.message = "printing in course"
    
    def action(self, braille_gui):
        braille_gui.ids.printingProgress.value+=1

        
class PrinterConnectionMessage(PrinterMessage):
    
    def __init__(self):
        self.message = "printing in course"
    
    def action(self, braille_gui):
        print (self.message)