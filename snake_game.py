from random import randint
from time import sleep, time

class Snake:
    def __init__(self, limits=tuple):
        self.xf, self.yf = limits
        self.mouth = randint(0, self.xf), randint(0, self.yf)
        self.body = [self.mouth]
        self.direction = None  # first move change this
        self.step = None
        self.life = True

        # define first move
        spaceToMove = {}
        spaceToMove['right'] = self.xf - self.mouth[0]
        spaceToMove['left'] = self.mouth[0]
        spaceToMove['up'] = self.yf - self.mouth[1]
        spaceToMove['down'] = self.mouth[1]
        spaceToMove = sorted(spaceToMove.items(), key=lambda sp: sp[1], reverse=True)
        self.direction = spaceToMove[0][0]
        del spaceToMove

    def move(self, mvDir=str, foodposition=tuple):
        # verify current direction or last direction in memory
        # you cant reverse the snake
        if mvDir == 'up' and self.direction != 'down':
            self.step = 0, 1
            self.direction = mvDir
        elif mvDir == 'down' and self.direction != 'up':
            self.step = 0, -1
            self.direction = mvDir
        elif mvDir == 'left' and self.direction != 'right':
            self.step = -1, 0
            self.direction = mvDir
        elif mvDir == 'right' and self.direction != 'left':
            self.step = 1, 0
            self.direction = mvDir

        # new mouth position
        self.mouth = self.mouth[0]+self.step[0], self.mouth[1]+self.step[1]

        # you have food for me?
        if self.snakeEating(foodposition) == False:
            self.body.insert(0, self.mouth) # insert the mouth in the body
            self.body.pop() # remove last part of body
        elif self.snakeEating(foodposition) == True:
            self.body.insert(0, self.mouth) # just add mouth position

    def snakeEating(self, foodPosition=tuple):
        if foodPosition == self.mouth:
            return True
        else:
            return False

    def stillAlive(self):
        x, y = self.mouth
        if x < 0 or x > self.xf or y < 0 or y > self.yf: # is not in in board range
            self.life = False
        for point in self.body[1:]: # if the mouth touch the snake body
            if self.mouth == point:
                self.life = False


class Board:
    def __init__(self, limits = tuple):
        self.xlimit, self.ylimit = limits

    def terminalPrintPanel(self, snakebody=list, food=tuple, move='up'):  # cambiar a curses en el futuro
        p = [[' ' for i in range(self.xlimit+1)] for i in range(self.ylimit+1)]

        fx, fy = food
        p[self.ylimit-fy][fx] = '*'

        mouth = ''
        if move == 'up':
            mouth = 'v'
        elif move == 'down':
            mouth = '^'
        elif move == 'left':
            mouth = '>'
        elif move == 'right':
            mouth = '<'
        fx, fy = snakebody[0]
        p[self.ylimit-fy][fx] = mouth

        for points in snakebody[1:]:
            x,y = points
            p[self.ylimit-y][x] = 'O'
        print('  .'*(self.xlimit+2))
        for rows in p:
            print('  .', end='')
            for cols in rows:
                print(cols, end=' .')
            print()
        print('\n\n')

    def terminalEndGame(self):
        print('\t\tthe end\t\t')


class LedPrint:
    def __init__(self, dimensions=tuple, frec=int):
        from timehandler import CycleHandler
        from raspberrypi import RPiSimulator
        self.dimensions = dimensions[0]+1
        self.sleep = sleep
        self.IO = RPiSimulator()
        self.cycle = CycleHandler(self.IO.setLed, frec=frec)

    def __makeParts(self, snakemouth=tuple, snakebody=list, direction=str) -> list:
        # Para hacer las partes de la serpiente, es decir el cuerpo en varias partes
        lastPoint = snakemouth
        # las partes seran una lista de puntos, y las partes estaran en una lista
        bodyparts = [[]]
        partNumber = 0  # inicio la cantidad de partes

        # Defino hacia donde esta mirando la serpiente con este metodo
        # Reviso el segundo punto de la lista y lo comparo con la boca para saber el eje
        if direction in ['left', 'right']:
            axis = 'X'
        elif direction in ['up', 'down']:
            axis = 'Y'

        # Armo las partes y cada vez que cambio de eje creo otra
        for point in snakebody:
            if point[0] == lastPoint[0] and axis == 'X':
                bodyparts[partNumber].append(point)
            elif point[1] == lastPoint[1] and axis == 'Y':
                bodyparts[partNumber].append(point)
            else:  # cerrando una parte y creando otra. Cambiando de eje
                partNumber += 1
                bodyparts.append([])
                bodyparts[partNumber].append(point)
                if axis == 'Y': axis = 'X'
                elif axis == 'X': axis = 'Y'

            lastPoint = point  # actualizo el ultimo punto
        return bodyparts

    def show(self, snakemouth=tuple, snakebody=list, direction=str, food=tuple) -> None:
        if self.cycle.running == False:
            allParts = self.__makeParts(snakemouth, snakebody, direction)
            allParts.append([food])
            self.allParts = allParts

        self.cycle.runCycle(self.allParts)

    def stop(self):
        self.cycle.stopCycle()
        self.allParts == []

    def shutdown(self):
        self.IO.finishLeds()


class Food:
    def __init__(self, limits=tuple):
        self.__limits = limits # create only inside the board
        self.position = None # coordinates

    def newFood(self, snakeBody=list):
        xf, yf = self.__limits # limits
        self.position = (randint(0, xf), randint(0, yf))

        # if new food is created inside the snake
        if self.position in snakeBody:
                self.newFood(snakeBody) # create other (recursive)


class Control:
    def __init__(self):
        from pynput import keyboard
        self.keyboard = keyboard
        self.allowedKeys = ['left','right','up','down']
        self.pressed = [None]
        self.listener = None

    def on_press(self, key):
        key = str(key)[4:]
        if key in self.allowedKeys:
            self.pressed.pop()
            self.pressed.append(key)

    def on_release(self, key):
        pass

    def start(self):

        self.listener = self.keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def stop(self):
        self.listener.stop()
        self.pressed = None
        self.listener = None



# DEFINO VARIABLES PRINCIPALES
dim = 8  #  8 leds en x y 8 leds en y
limits = dim-1, dim-1  # usamos rango de 0 a 7
frec = 100 # hz para los leds
velocity = 1 # movimiento de serpiente por segundo

# object screen
screen = Board(limits)

# object snake
snake = Snake(limits)

# object food
food = Food(limits)

# object leds
leds = LedPrint(limits, frec)

# Game control
control = Control()

# moving snake
food.newFood(snake.body)
while snake.life:
    ti = time()
    # Obtiene el input del teclado y imprime la serpiente
    control.start()
    while time()-ti < 1/velocity:
        leds.show(snake.mouth, snake.body, snake.direction, food.position)
    leds.stop()

    # verifica si se ha colocado nueva direccion
    if control.pressed[-1] is None:
        snake.move(snake.direction, food.position)
    else:
        snake.move(control.pressed[-1], food.position)

    if snake.snakeEating(food.position) is True:
        food.newFood(snake.body)
        if velocity < 3:
            velocity *= 1.2

    snake.stillAlive()
else:
    leds.shutdown()
    control.stop()
    print("""
          THE END. SAMUEL IBARRA
          """)