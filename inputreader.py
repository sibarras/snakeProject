from time import sleep

class Control:
    def __init__(self):
        from pynput import keyboard
        self.keyboard = keyboard
        self.allowedKeys = ['left','right','up','down']
        self.pressed = None
        self.listener = None

    def on_press(self, key):
        key = str(key).lstrip('Key.')
        if key in self.allowedKeys:
            self.pressed = key

    def on_release(self, key):
        pass

    def start(self):
        self.pressed = None
        self.listener = self.keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def stop(self):
        self.listener.stop()
        self.listener = None

control = Control()
control.start()
sleep(5)
control.stop()
print(control.pressed)
control.start()
sleep(5)
control.stop()
print(control.pressed)
print("WELL DONE")