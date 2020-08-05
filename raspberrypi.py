# class PinsArray:
#     import RPi.GPIO as GPIO
#     pos_pin = [24, 22, 18, 16, 23, 21, 19, 15]
#     neg_pin = [40, 38, 36, 32, 37, 35, 33, 31]

#     def __init__(self, dimensions=8, GPIO=GPIO, pos_pin=pos_pin, neg_pin=neg_pin):
#         self.pos_pin = pos_pin
#         self.neg_pin = neg_pin
#         self.GPIO = GPIO
#         self.dimensions = dimensions
#         GPIO.setmode(GPIO.BOARD)

#         for pin in pos_pin:
#             GPIO.setup(pin, GPIO.OUT)
#         for pin in neg_pin:
#             GPIO.setup(pin, GPIO.OUT)

#         for pos in range(self.dimensions):
#             GPIO.output(pos_pin[pos], False)
#             GPIO.output(neg_pin[pos], True)


#     def setLed(self, coordinates=tuple, state=str):
#         xpos, yneg = coordinates
#         if state == 'ON':
#             self.GPIO.output(self.pos_pin[xpos], True)
#             self.GPIO.output(self.neg_pin[yneg], False)
#         elif state == 'OFF':
#             self.GPIO.output(self.pos_pin[xpos], False)
#             self.GPIO.output(self.neg_pin[yneg], True)

#     def finishLeds(self):
#         for pos in range(self.dimensions):
#             self.GPIO.output(self.pos_pin[pos], False)
#             self.GPIO.output(self.neg_pin[pos], False)

#from time import sleep

class RPiSimulator:
    pos_pin = [24, 22, 18, 16, 23, 21, 19, 15]
    neg_pin = [40, 38, 36, 32, 37, 35, 33, 31]


    def __init__(self, dimensions=8):
        self.pos_pin = RPiSimulator.pos_pin
        self.neg_pin = RPiSimulator.neg_pin
        self.dimensions = dimensions
        
        # this is the decoder for the rpi representation of the code
        class GPIO:

            @classmethod
            def __init__(cls, pos_pin=self.pos_pin, neg_pin=self.neg_pin, dim=self.dimensions):
                cls.pos_pin = RPiSimulator.pos_pin
                cls.neg_pin = RPiSimulator.neg_pin
                cls.ledMtx = [["[ ]" for i in range(dim)] for j in range(dim)]
                cls.energized = [["[ ]" for i in range(dim)] for j in range(dim)]

            @classmethod
            def output(cls, outputNumber=int, state=bool):
                if outputNumber in cls.pos_pin: # x axis
                    currentPin = cls.pos_pin.index(outputNumber)
                    action = 'OneColPos'
                elif outputNumber in cls.neg_pin: # y axis
                    currentPin = cls.neg_pin.index(outputNumber)
                    action = 'OneRowNeg'

                if action == 'OneRowNeg':
                    for i in range(len(cls.ledMtx)):
                        if state == False:
                            cls.ledMtx[currentPin][i] = "[O]"
                        elif state == True:
                            cls.ledMtx[currentPin][i] = "[ ]"
                if action == 'OneColPos':
                    for i in range(len(cls.ledMtx)):
                        if state == True:
                            cls.ledMtx[i][currentPin] = "[O]"
                        elif state == False:
                            cls.ledMtx[i][currentPin] = "[ ]"
                cls.display()
            
            @classmethod
            def display(cls):
                xon, yon = [], []
                xoff, yoff = [], []
                dim = len(cls.ledMtx)
                counton, countoff = 0, 0
                # Search for index where you have the row on
                for y in range(dim):
                    if cls.ledMtx[y].count("[O]") == dim:
                        yon.append(y)
                    elif cls.ledMtx[y].count("[ ]") == dim:
                        yoff.append(y)
                    # search in cols
                    for x in range(dim):
                        if cls.ledMtx[x][y] == "[O]":
                            counton += 1
                        elif cls.ledMtx[x][y] == "[ ]":
                            countoff += 1
                    if counton == dim:
                        xon.append(y)
                    elif countoff == dim:
                        xoff.append(y)
                    countoff = 0
                    counton = 0

                for row in yon:
                    for col in xon:
                        cls.energized[row][col] = "[O]"
                for row in yoff:
                    for col in xoff:
                        cls.energized[row][col] = "[ ]"

                for row in reversed(cls.energized):
                    for led in row:
                        print(f"{led}", end='')
                    print()
                print('\n\n')
        self.GPIO = GPIO()
        
# esto se debe descomentar cuando estes en la rpi. ES PARA INICIALIZAR LEDS
        # for pos in range(self.dimensions):
        #     self.GPIO.output(self.pos_pin[pos], False)
        #     self.GPIO.output(self.neg_pin[pos], True)

    def setLed(self, coordinates=tuple, state=str):
        xpos, yneg = coordinates
        if state == 'ON':
            self.GPIO.output(self.pos_pin[xpos], True)
            self.GPIO.output(self.neg_pin[yneg], False)
        elif state == 'OFF':
            self.GPIO.output(self.pos_pin[xpos], False)
            self.GPIO.output(self.neg_pin[yneg], True)

    def finishLeds(self):
        for pos in range(self.dimensions):
            self.GPIO.output(self.pos_pin[pos], False)
            self.GPIO.output(self.neg_pin[pos], False)



# IO = RPiSimulator() #funciona perfecto
# positions = [(1,2),(1,3),(1,4),(1,5),(1,6),(2,6),(3,6),(4,6)]

# # analizar si se puede implementar lo de imprimir pedazos de serpiente
# for i in range(300):
#     for position in positions:
#         IO.setLed(position, 'ON')
#         sleep(0.01)
#         IO.setLed(position, 'OFF')

# #descomentar
# # IO.finishLeds()
