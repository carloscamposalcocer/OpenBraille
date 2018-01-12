# OpenBraille
Software for controlling an open source braille embosser

Follow the instructions at :
https://www.instructables.com/id/Open...

Facebook page:
https://www.facebook.com/OpenBraille-...

Download files at:
https://www.thingiverse.com/thing:2586738


# Instructions

There are two parts to the software, you will need to install the firmware on your arduino and a software for your computer


# Arduino

OpenBraille uses the firmware for 3Dprinters (Marlin firmware). If you use the exact same hardware as I did you can use the files included. Otherwise you will need to modify a few parameters. Most likely you'll have to change the steps-per-unit depending on the stepper motor installed on your printer. You will find the following line on the file Marlin/Configuration.h


#define DEFAULT_AXIS_STEPS_PER_UNIT    {800, 800, 167,500}     // line 479 


                                        X,     Y,   Z, E0
                                        
Where the first 800 is the steps to move top cariage by 1 mm, the second 800 is the steps to move the bottom cariage, the 167 is the steps to move the paper and the 500 is not used.
For other configurations you will have to read on how to configure a 3dprinters firmware. 


# Computer's Software

As the arduino is using the firmware from a 3dprinter, we need to send G-code the braille embosser for it to work. So the sofware reads letters from the user and it transforms them into a series of codes for the printer to move acordingly.
On the folder writer, there are two differents programs: 
      
      writer.py uses the terminal to send the g-code 
      brailleGUI.py User Interface for the braille printer
      
For them to work you will need to install the pyserial library:
  Change directory to pyserial-master/ and use the command
      
      python setup.py install
      
  This will install the library to communicate with the arduino
  
  
For the User Interface you will need to install kivi:

https://kivy.org/#home

Once the User Interface is launched, you will need to connect to the printer, then you can send the print.

Happy embossing


# Credits

Special thanks to David Pache for his contribution on the User Interface!!
https://www.linkedin.com/in/davidpache/

Y muchas gracias por su ayuda!


test
