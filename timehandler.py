# time handler
from time import sleep, time, time_ns
from os import sys

# blink without sleep

toff = 0.5 # ton en segundos
ton = 1 # toff en segundos
flags = 0b01 # estado de flag en off
flag_on, flag_off = 0b10, 0b01
T = ton + toff # tiempo total del ciclo

cycles = 6 # cantidad de ciclos
tfinal = time() + T*cycles # tiempo total para terminar

t = time()
while tfinal > time() or flags & flag_on: # stay on in this cases

    if (time()-t > toff) and flags & flag_off: # only if bit off is 1

        print('ON\n\n\n\n\n')
        flags ^= 3
        t = time()

    if (time()-t > ton) and flags & flag_on: # only if bit on is 1

        print('OFF\n\n\n\n\n')
        flags ^= 3
        t = time()


