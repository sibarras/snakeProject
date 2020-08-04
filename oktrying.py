import curses
from time import time, sleep
import io

t1 = time()//1
print(t1)
sleep(1)
t2 = time()//1
print(t2-t1)

input('press any key to continue...')


key = None
screen = curses.initscr()  # inicia la instancia de la nueva pantalla
curses.noecho()  # no devolver a la pantalla el valor que fue ingresado, ya que 
# curses.cbreak()  # romper la ejecucion solo con un caracter, sin necesitar enter
screen.keypad(True) # obtener valores de las teclas especiales, para poder hacer uso de ellas

#curses.halfdelay(10)
key = screen.getch()

# curses.nocbreak()
screen.keypad(False)

curses.echo()
curses.endwin()

print(key)
