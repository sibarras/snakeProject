# time handler
from time import sleep, time

# blink without sleep
class CycleHandler:
    def __init__(self, target, power=90, frec=60):
        # Funciones a ejecutar para encender y apagar
        self.target = target
        self.power = power
        self.frec = frec
        self.period = 1/frec

        self.TON = self.period * self.power/100 # ton en segundos
        self.TOFF = self.period - self.TON # toff en segundos
        self.running = False


    def runCycle(self, processList=list) -> None:
        if self.running == False:
            n = len(processList)
            self.processList = processList
            self.TOFF /= n
            self.TON /= n
            self.running = True

        for process in processList:
            for point in process:
                self.target(point, 'ON')
            sleep(self.TON)
            for point in process:
                self.target(point, 'OFF')
            sleep(self.TOFF)


    def stopCycle(self):  # Solo utilizar si la serpiente come algo o muere o se mueve
        self.TON *= len(self.processList)
        self.TOFF *= len(self.processList)

        self.processList = None
        self.running = False