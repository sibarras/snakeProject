from random import randint
from time import sleep
import keyboard # deseo eliminar esta libreria en un futuro
from raspberrypi import RPiSimulator


class Snake:
    def __init__(self, limits=tuple):
        self.xf, self.yf = limits
        self.mouth = randint(0, self.xf), randint(0, self.yf)
        self.body = [self.mouth]
        self.direction = None
        self.step = None
        self.life = True

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
        if self.eat(foodposition) == False:
            self.body.insert(0, self.mouth) # insert the mouth in the body
            self.body.pop() # remove last part of body
        elif self.eat(foodposition) == True:
            self.body.insert(0, self.mouth) # just add mouth position

    def eat(self, foodPosition=tuple):
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
    def __init__(self, xlim=int, ylim=int):
        self.xlimit = xlim - 1
        self.ylimit = ylim - 1

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
    def __init__(self, dimensions=8):
        from time import sleep
        from raspberrypi import RPiSimulator
        self.dimensions = dimensions
        self.sleep = sleep
        self.IO = RPiSimulator()

    def makeParts(self, snakemouth=tuple, snakebody=list):
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


# object wall
dim = int(input('Inserta la cantidad de filas y columnas: '))
screen = Board(dim, dim)
limits = screen.xlimit, screen.ylimit

# object snake
snake = Snake(limits)

# object food
food = Food(limits)
food.newFood(snake.body)

# define first move (choose the largest distance)
spaceToMove = {}
spaceToMove['right'] = limits[0] - snake.mouth[0]
spaceToMove['left'] = snake.mouth[0]
spaceToMove['up'] = limits[1] - snake.mouth[1]
spaceToMove['down'] = snake.mouth[1]
spaceToMove = sorted(spaceToMove.items(), key=lambda sp: sp[1], reverse=True)
snake.direction = spaceToMove[0][0]
del spaceToMove

# moving snake
while snake.life:
    # imprime la pantalla
    screen.terminalPrintPanel(snake.body, food.position, snake.direction)
    userKey = ''

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

    if snake.eat(food.position) is True:
        food.newFood(snake.body)

    snake.stillAlive()
else:
    print("""
          THE END. SAMUEL IBARRA
          """)
