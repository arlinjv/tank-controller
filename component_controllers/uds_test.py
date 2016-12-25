import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24

print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(1)

try:
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO)==0:
		pass
	pulse_start = time.time()

	while GPIO.input(ECHO)==1:
		pass
	pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start

	print "pulse duration: ",pulse_duration 

	distance = pulse_duration * 17150

	distance = round(distance, 2)

	print "Distance:",distance,"cm"
	
except Exception, e:
	print repr(e)

finally: GPIO.cleanup()
