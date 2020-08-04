# trying 2
class You:
    J = 'called from class'

    @classmethod
    def __init__(cls, nums=1):
        print(cls.J)
        cls.J += ' plus one'

You()
You()
You()
You()


lst = [1,2,3,'a', 'km']

print(lst.index(3))

class LedPrint:
    def __init__(self, dimensions=8):
        from time import sleep
        from raspberrypi import RPiSimulator
        self.dimensions = dimensions
        self.sleep = sleep
        self.IO = RPiSimulator()

    def makeParts(self, snakemouth=tuple, snakebody=list) -> list:
        lastPoint = snakemouth
        bodyparts = [[]]
        partNumber = 0
        if snakebody[1][0] == lastPoint[0]:
            axis = 'X'
        elif snakebody[1][1] == lastPoint[1]:
            axis = 'Y'
        for point in snakebody:
            if point[0] == lastPoint[0] and axis == 'X':
                bodyparts[partNumber].append(point)
            elif point[1] == lastPoint[1] and axis == 'Y':
                bodyparts[partNumber].append(point)
            else:
                partNumber += 1
                bodyparts.append([])
                bodyparts[partNumber].append(point)
                if axis == 'Y': axis = 'X'
                elif axis == 'X': axis = 'Y'
            lastPoint = point
        return bodyparts

    def show(self, snakemouth=tuple, snakebody=list, food=tuple):

        bodyParts = self.makeParts(snakemouth, snakebody)
        bodyParts.append([food])
        for part in bodyParts:
            for point in part:
                self.IO.setLed(point, 'ON')
            self.sleep(0.1)
            for point in part:
                self.IO.setLed(point, 'OFF')


food = (1,1)
mouth = (4,2)
body = [
    (4,2),
    (4,3),
    (4,4),
    (4,5),
    (5,5),
    (6,5),
    (6,4),
    (6,3),
    (6,2),
    (5,2)
]
io = LedPrint()
io.show(mouth, body, food)