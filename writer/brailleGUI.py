import time
import sys
from  multiprocessing import *

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock


from printermessage import *
from printercontrolmessage import *



import braille
import serial.tools.list_ports

class BrailleGui(Widget):
    
    def __init__(self) :
        super(BrailleGui,self).__init__()
        self.dictPort = {}
        self.connectedPrinter = False
        self.braillePrinter = None
        
        if __name__ == '__main__':
#            self.queue = multiprocessing.Queue()
            self.gui_connection, printer_proc_connection = Pipe()
            Clock.schedule_interval(self.update, 1)  ## update state from printer
            self.printer_process = Process(target=braille_control,args=(printer_proc_connection,))
            self.printer_process.start()
    
    def sendTextToPrinter(self):
        print('sendTextToPrinter')
        
        if (not self.connectedPrinter):
            print ("no printer connected.")
            return
        
        mystring = self.ids.textToSend.text
        print ("The string to print : " + mystring)
        self.ids.printingProgress.max=len(mystring)
#        self.ids.printingProgress.value= len(mystring)

        self.ids.printingProgress.value = 0 
    
        if __name__ == '__main__':
            ReservedPrinter().action(self)
            self.gui_connection.send(PrintText(mystring))
        #    self.printingProcess = #multiprocessing.Process(target=braillePrint,args=(mystring,self.queue, self.braillePrinter,))
            #self.printingProcess.start()
    
    def update(self,a):
       while (self.gui_connection.poll()) :
           message = self.gui_connection.recv()
           message.action(self)

    def close(self):
        self.gui_connection.send(Close())

        while (self.printer_process.is_alive()) :
            time.sleep(.05)

        print ("All processes are closed.")
    

    def selectOutputOptions(self):
        self.ids.outputOptions.clear_widgets()
        
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            btnOutput = Button(text=p.description, height=20, font_size=25)
            self.dictPort[p.description] = p.device
            self.ids.outputOptions.add_widget(btnOutput)
            btnOutput.bind(on_press=lambda  p=p : self.changeOutput(p.text))
        self.ids.outputOptions.pos =  ( self.ids.selectOutput.x, self.ids.toolBar.y - self.ids.outputOptions.height)    
            
    
    def changeOutput(self,text):
        currentOutput = self.dictPort[text]
        print (currentOutput)
        self.ids.outputOptions.clear_widgets()
        ReservedPrinter().action(self)
        self.gui_connection.send(ConnectPrinter(currentOutput))
        
#        self.printingProcess = multiprocessing.Process(target=connectPrinter, args=(self.queue,self.currentOutput))
        
#        self.printingProcess.start()

class PrinterController :
    def __init__ (self, pipe):
        self.pipe = pipe
        self.braillePrinter = None
        self.closing = False
        
    def connectPrinter (self,currentOutput) :
        try   :
                print ("connection to the printer ...")
                self.braillePrinter = braille.Braille(currentOutput)
                
                self.pipe.send(ConnectedPrinter())
                
        except Exception as inst:
                self.pipe.send(UnconnectedPrinter())
                print ("no connection to the printer")
                print (inst.args)
        
        self.pipe.send(FreedPrinter())
        

    def braillePrint(self, mystring):
        self.braillePrinter.open_serial()
        self.braillePrinter.init_printer()

        for letter in mystring:
            print ("letter : " + letter)
            digits = self.braillePrinter.letters(letter)	        #Transform letters into numbers for the encoder
            self.braillePrinter.emboss(digits)					#Routine for embossing 
            print(digits)
            self.pipe.send(ProgressMessage())

        self.braillePrinter.eject_paper()
        self.braillePrinter.close_serial()
        self.pipe.send(FreedPrinter())


def braille_control (pipe):
    printer_controller  = PrinterController(pipe)
    
    while(not printer_controller.closing): # replace the boolean
        while (pipe.poll()):
            message = pipe.recv()
            message.action(printer_controller)

        
class BrailleApp(App):
    
    def build(self):
        self.braille_gui = BrailleGui()
        
        return self.braille_gui
    
    def on_stop(self):
        self.braille_gui.close()
        

if __name__ == '__main__':
    a = Message()
    BrailleApp().run()