#!/usr/bin/python3
from pynput.keyboard import Key, Listener 

pressed = []
def on_press(key):
    pressed.append(key)
    print("{}".format(key))

def on_release(key):
    if key == Key.esc:
        print(pressed)
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
