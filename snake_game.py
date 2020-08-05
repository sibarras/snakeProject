from random import randint
from time import sleep
from pynput.keyboard import Key, Listener  # Aplicar
import keyboard # deseo eliminar esta libreria en un futuro

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
        for points in self.body[1:]: # if the mouth touch the snake body
            if self.mouth == points:
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
    def __init__(self, dimensions=tuple):
        from timehandler import CycleHandler
        from raspberrypi import RPiSimulator
        self.dimensions = dimensions[0]+1
        self.sleep = sleep
        self.IO = RPiSimulator()
        self.cycle = CycleHandler(self.IO.setLed)

    def __makeParts(self, snakemouth=tuple, snakebody=list) -> list:
        # Para hacer las partes de la serpiente, es decir el cuerpo en varias partes
        lastPoint = snakemouth
        # las partes seran una lista de puntos, y las partes estaran en una lista
        bodyparts = [[]]
        partNumber = 0  # inicio la cantidad de partes
        
        # Defino hacia donde esta mirando la serpiente con este metodo
        # Reviso el segundo punto de la lista y lo comparo con la boca para saber el eje
        if snakebody[1][0] == lastPoint[0]:
            axis = 'X'
        elif snakebody[1][1] == lastPoint[1]:
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
    
    def show(self, snakemouth=tuple, snakebody=list, food=tuple) -> None:
        if self.cycle.running == False:
            allParts = self.__makeParts(snakemouth, snakebody)
            self.allParts = allParts.append([food])
        
        self.cycle.runCycle(self.allParts)

    def stop(self):
        self.cycle.stopCycle()
        self.allParts == []

    def shutdown(self):
        self.cycle.stopCycle()
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


# DEFINO VARIABLES PRINCIPALES
dim = 8  #  8 leds en x y 8 leds en y
limits = dim-1, dim-1  # usamos rango de 0 a 7

# object screen
screen = Board(limits)

# object snake
snake = Snake(limits)

# object food
food = Food(limits)

# object leds
leds = LedPrint(limits)

# moving snake
food.newFood(snake.body)
while snake.life:
    # imprime la pantalla -- Cambiar para usar leds
    screen.terminalPrintPanel(snake.body, food.position, snake.direction)
    
    userKey = ''
    # Hacer esto del start y stop recording con el time() y los tiempos de inicio y fin.
    keyboard.start_recording()
    sleep(0.5)
    listOfKeys = keyboard.stop_recording()

    if len(listOfKeys) > 0:
        userKey = str(listOfKeys[0])[14:][:-6]
    del listOfKeys
    if userKey == 'up' or userKey == 'down' or userKey == 'left' or userKey == 'right':
        snake.move(userKey, food.position)
    else:
        snake.move(snake.direction, food.position)

    if snake.snakeEating(food.position) is True:
        food.newFood(snake.body)

    snake.stillAlive()
else:
    print("""
          THE END. SAMUEL IBARRA
          """)
