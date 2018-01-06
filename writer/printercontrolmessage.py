class ControlPrinterMessage :
    def action (self) :
        pass

class ConnectPrinter(ControlPrinterMessage) :
    def __init__(self, connection_output):
        self.output=connection_output
    
    def action(self,printer_controler) :
        printer_controler.connectPrinter(self.output)
        
class PrintText(ControlPrinterMessage) :
    def __init__(self, mystring):
        self.mystring=mystring
    
    def action(self,printer_controler) :
        printer_controler.braillePrint(self.mystring)
        
class Close(ControlPrinterMessage) :
    def action(self,printer_controler) :
        printer_controler.closing = True