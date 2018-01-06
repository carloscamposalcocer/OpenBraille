import braille

brai = braille.Braille('COM4')
brai.init_printer()
#ser.write(b'G0 X10 Y20 \n')

while True:
    mystring = input('Type something:')    # Reads line from user
    print(brai.ser.readline())
    for letter in mystring:					
        digits = brai.letters(letter)		#Transform letters into numbers for the encoder
        brai.emboss(digits)					#Routine for embossing 
        print(digits)

            #x = x + xstep

# for letter in mystring:
#     if letter ==``
