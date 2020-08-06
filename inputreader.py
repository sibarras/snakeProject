#!/usr/bin/python3
from pynput.keyboard import Key, Listener

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
    def start(cls):
        cls.pressed = None
        cls.running = True
        cls.end = False
        with Listener(on_press=cls.on_press, on_release=cls.on_release) as listener:
            listener.join()


    @classmethod
    def stop(cls):
        cls.end = True

from time import time, sleep
ti = time()
while time()-ti < 10:
    sleep(1)
    print(time()-ti)
    if not Keylogger.running:
        Keylogger.start()
    if Keylogger.pressed != None:
        break
Keylogger.stop()