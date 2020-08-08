
class RPiSimulator:
    pos_pin = [24, 22, 18, 16, 23, 21, 19, 15]
    neg_pin = [40, 38, 36, 32, 37, 35, 33, 31]


    def __init__(self, dimensions=8):
        import RPi.GPIO as GPIO
        self.pos_pin = RPiSimulator.pos_pin
        self.neg_pin = RPiSimulator.neg_pin
        self.dimensions = dimensions
        self.GPIO = GPIO

        self.GPIO.setmode(GPIO.BOARD)
        self.GPIO.setwarnings(False)
        for pin in self.pos_pin:
            GPIO.setup(pin, GPIO.OUT)
        for pin in self.neg_pin:
            GPIO.setup(pin, GPIO.OUT)

        for pos in range(self.dimensions):
            self.GPIO.output(self.pos_pin[pos], False)
            self.GPIO.output(self.neg_pin[pos], True)

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


if __name__ == '__main__':
    from time import sleep
    IO = RPiSimulator() #funciona perfecto
    positions = [(1,2),(1,3),(1,4),(1,5),(1,6),(2,6),(3,6),(4,6)]

    # analizar si se puede implementar lo de imprimir pedazos de serpiente
    for i in range(300):
        for position in positions:
            IO.setLed(position, 'ON')
            sleep(0.01)
            IO.setLed(position, 'OFF')

    # #descomentar
    IO.finishLeds()