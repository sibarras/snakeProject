#!/usr/bin/python3
#from pynput.keyboard import Key, Listener
from pynput import keyboard
# vamos a utilizar la condicion de tener o no presionada una tecla para
# usarlo como on off del keylogger y cada vez que la serpiente se mueva lo
# volvemos a activar
class Keylogger:
    pressed = None
    end = False
    running = False

    @classmethod
    def on_press(cls, key):
        key = str(key).lstrip('Key.')
        if key in ['up','down','left','right']:
            cls.stop()
            cls.pressed = key
            print('finish '+key)

    @classmethod
    def on_release(cls, key):
        if cls.end == True:
            cls.running = False
            return False

    @classmethod
    def start(cls, time):
        cls.pressed = None
        cls.running = True
        cls.end = False
        with keyboard.Events() as events:
            pressed = events.get(time)
            if pressed is None:
                print('you dont press any key')
            else:
                print('Recieved event '+pressed)


    @classmethod
    def stop(cls):
        cls.running = False
        cls.end = True

# from time import time, sleep
# ti = time()
# while time()-ti < 10:
#     sleep(1)
#     print(time()-ti)
#     if not Keylogger.running:
#         Keylogger.start(1.0)
#     if Keylogger.pressed != None:
#         break
# Keylogger.stop()
with keyboard.Events() as events:
            event = events.get(1.0)
            if event is None:
                print('you dont press any key')
            else:
                print('Recieved event '+ event)