import Adafruit_DHT, json, time
import RPi.GPIO as GPIO
from threading import Timer
from logger import Logger
from vesync import VesyncApi

GPIO.setmode(GPIO.BCM)
sensor = Adafruit_DHT.DHT22
pin = 4
trans = 17
GPIO.setup(trans, GPIO.OUT)
GPIO.output(trans, 1)
vesync_creds = json.loads(open('/home/pi/creds/vesync.json','r').read())
vsapi = VesyncApi(vesync_creds['user'],vesync_creds['password'])
humid_id = '0539c140-a3d0-484f-9b24-c003424f94c1'
fan_id = 'ad9708cf-1784-4d61-885a-7aa3f831b372'
heat_id = '26f8d44d-77a1-4235-8f75-dcc99ae21f1b'
min_temp = 76
max_temp = 78
min_hum = 85
max_hum = 92

class RepeatedTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
		self._timer	 = None
		self.interval   = interval
		self.function   = function
		self.args	   = args
		self.kwargs	 = kwargs
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

def status(id):
	return vsapi.get_detail(id)['deviceStatus']

def heat_off():
	if status(heat_id) == 'on':
		vsapi.turn_off(heat_id)
	return

def heat_on():
	if status(heat_id) == 'off':
		print('HEATING')
		vsapi.turn_on(heat_id)
	return

def fan_off():
	if status(fan_id) == 'on':
		vsapi.turn_off(fan_id)
	return

def fan_on():
	if status(fan_id) == 'off':
		print('FANNING')
		vsapi.turn_on(fan_id)
	return

def humidifier_off():
	if status(humid_id) == 'on':
		vsapi.turn_off(humid_id)
	return

def humidifier_on():
	if status(humid_id) == 'off':
		print('FOGGING')
		vsapi.turn_on(humid_id)
	return

def measure():
	state = GPIO.input(trans)
	if state == False:
		time.sleep(1)
		GPIO.output(trans, 1)
		time.sleep(1)
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is None or temperature is None:
		print('bad sensor read')
		my_logger.log_error('bad read', 'h={},t={}'.format(humidity, temperature))
		GPIO.output(trans, 0)
		fan_off()
		return
	ftemp = (temperature * 1.8) + 32
	my_logger.log(humidity, ftemp)
	
	if ftemp > max_temp:
		print('too hot:{}'.format(ftemp))
		heat_off()
		fan_on()
	elif ftemp < min_temp:
		print('too cold:{}'.format(ftemp))
		heat_on()
		fan_off()
	else:
		print('perfect temp:{}'.format(ftemp))
		heat_off()
		fan_off()

	if humidity > max_hum:
		print('too humid:{}'.format(humidity))
		humidifier_off()
		fan_on()
	elif humidity < min_hum:
		print('too dry:{}'.format(humidity))
		fan_off()
		humidifier_on()
	else:
		print('perfect moint:{}'.format(humidity))
		humidifier_off()
		fan_off()

print ("starting...")
print ("communicating with vsapi:")
for dev in vsapi.get_devices():
	print ('{}:{}:{}'.format(dev['deviceName'],dev['cid'],dev['connectionStatus']))
my_logger = Logger('chamber')
my_logger.log_error('startup', None)
rt = RepeatedTimer(30, measure) 
