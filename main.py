import Adafruit_DHT
from threading import Timer
from time import sleep
from logger import Logger

sensor = Adafruit_DHT.DHT22
pin = 4

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def measure():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    print('Humidity:{}, Temp:{}'.format(humidity, temperature))

print "starting..."
rt = RepeatedTimer(1, measure) # it auto-starts, no need of rt.start()
try:
    sleep(20) # your long-running job goes here...
finally:
    rt.stop() # better in a try/finally block to make sure the program ends!