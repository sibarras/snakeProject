# time handler
from time import sleep, time, time_ns

# blink without sleep
class CycleHandler:
    def __init__(self, target, power=95, frec=60):
        # Funciones a ejecutar para encender y apagar
        self.target = target
        self.power = power
        self.frec = frec
        self.period = 1/frec
        
        self.TON = self.period * self.power # ton en segundos
        self.TOFF = self.period - self.TON # toff en segundos
        self.timeStart = 0
        self.timeRunning = 0
        self.running = False
        
        # Flags tienen el orden on off
        self.flags = 0b01 # estado de flag en off
        self.flag_on, self.flag_off = 0b10, 0b01 # modos de la variable en off y en on
    
    def runCycle(self, processList=list) -> None:
        if self.running == False:
            n = len(processList)
            self.processList = processList
            
            self.timeRunning = time()
            self.timeStart = time()
            
            # self.period /= n  # No se usa esto porque se utiliza el periodo completo en el while
            self.TOFF /= n
            self.TON /= n
            
            self.running = True

        for process in processList:
            while time() - self.timeRunning < self.period and self.flags & self.flag_off:
                if (time() - self.timeRunning > self.TOFF) and self.flags & self.flag_off: # only if bit off is 1
                    for point in process:
                        self.target(point, 'ON')
                    self.flags ^= 0b11  # cambia el flag a on
                    self.timeRunning = time()

                if (time()-self.timeRunning > self.TON) and self.flags & self.flag_on: # only if bit on is 1
                    for point in process:
                        self.target(point, 'OFF')
                    self.flags ^= 0b11  # cambia el flag a off
                    self.timeRunning = time()

    def stopCycle(self):  # Solo utilizar si la serpiente come algo o muere o se mueve
        # self.period *= len(self.processList)  # no se usa porque se usa el ciclo completo
        self.TON *= len(self.processList)
        self.TOFF *= len(self.processList)
        
        self.timeRunning = 0
        self.timeStart = 0
        
        self.processList = None
        self.running = False
