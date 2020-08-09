from pynput import keyboard
from time import time, sleep

vel = 0.5
kb = keyboard.Controller()
pressed = None
ti = time()
with keyboard.Events() as events:

    kb.release(keyboard.Key.space)
    for event in events:
        if str(event.key).lstrip('Key.') in ['up', 'down', 'left', 'right']:
            pressed = str(event.key).rstrip('Key.')
        if time() - ti > 1/vel:
            break 
        # Do the snake printing
        kb.release(keyboard.Key.space)

print('new direction is {}'.format(pressed)) # pressed variable have the direction or None
