import serial
import time


class Braille():
    def __init__(self,COM):  #initialises the braille printer, use COM as serial port
        self.xstep = 2.5
        self.zstep = 10
        self.xmin = 20
        self.xsize = 150
        self.speed = 1000
        self.x = 0
        self.y = 0
        self.z = 30
        self.ser = serial.Serial(COM, '250000', timeout=2)

    def init_printer(self):
        self.readall()
        self.write('G28')                   # home all
        self.x = 0;
        self.y = 0;
        self.z = 0;
        self.write('M211 Z1 S0')            # disable the z endStop
        self.move()

    def open_serial(self):
        if (not self.ser.is_open) :
            self.ser.open()
    
    def close_serial(self):
        if (self.ser.is_open) :
            self.ser.close()
    
    def servo(self,number):                        # move servo to position 0-7
        self.write('M400')
        self.write('M280 P0 S' + str(self.servo_number(number)))

    def servo_number(self,number):                 # Calibration of the servo position from 0-7 to degres
        return {
            0: 0,
            1: 80,
            2: 40,
            3: 125,
            4: 20,
            5: 105,
            6: 60,
            7: 150,
        }[number]

    def letters(self,letter):					#Transforms the letters into numbers for the encoder
        return{
            'a' : [1,0],
            'b' : [3,0],
            'c' : [1,1],
            'd' : [1,3],
            'e' : [1,2],
            'f' : [3,1],
            'g' : [3,3],
            'h' : [3,2],
            'i' : [2,1],
            'j' : [2,3],
            'k' : [5,0],
            'l' : [7,0],
            'm' : [5,1],
            'n' : [5,3],
            'o' : [5,2],
            'p' : [7,1],
            'q' : [7,3],
            'r' : [7,2],
            's' : [6,1],
            't' : [6,3],
            'u' : [5,4],
            'v' : [7,4],
            'x' : [5,5],
            'y' : [5,7],
            'z' : [5,6],
            ' ' : [0,0],
        }.get(letter, [7, 7])
    x = 0

    def write(self,line):                           ## Serial write to the arduino
        print(line)
        self.ser.write((line+' \n').encode())
        response = ' : ' + self.ser.readline().decode()
        print(response)
        while response.find('unknown') != -1:
            self.ser.write((line + ' \n').encode())
            response = ' : ' + self.ser.readline().decode()
            print("reprinting line : " + line)
        while response.find('busy') != -1:
            time.sleep(1)
            response = ' : ' + self.ser.readline().decode()
            print(response)




    def move(self):						
        self.write('G1' + ' X' + str(self.x) + ' Y' + str(self.y) + ' Z' + str(self.z) + ' F' + str(self.speed))
        #print('G0' + ' X' + str(self.x) + ' Y' + str(self.y) + ' Z' + str(self.z))

    def eject_paper(self):
        self.x = self.x - 30
        self.move()
        self.z = self.z + 50
        self.move()

    def emboss(self,digits):							#routine for embossing letters
        if self.x < self.xmin:
            self.y = self.xmin
            self.move()
            self.x = self.xmin - 2*self.xstep
            self.move()
        if self.x > self.xsize:
            self.x = self.x - 3*self.xstep
            self.x = self.xmin - 3*self.xstep
            self.y = self.xmin
            self.move()
            self.z = self.z + self.zstep
            self.move()
        for digit in digits:
            if digit==0:
                self.x = self.x + self.xstep
                self.y = self.y + self.xstep
                self.move()
            else:
                self.servo(digit)
                self.y = self.y + self.xstep
                self.move()
                self.x = self.y + 2*self.xstep
                self.move()
                self.x = self.y - 3*self.xstep
                self.move()
        self.x = self.x + self.xstep
        self.y = self.y + self.xstep
        self.move()

    def readall(self):										#Clears the buffer
        self.ser.readline()
        while self.ser.in_waiting != 0:
            print(self.ser.readline().decode("utf-8"))


# abcdefghijklmnopqrstuvxyz



