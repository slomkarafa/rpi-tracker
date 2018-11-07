import RPi.GPIO as GPIO
import time
from motor import Motor

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(17, GPIO.OUT)

#pwm = GPIO.PWM(17,100)
#pwm.start(0)
try:
    x = 1
    motor = Motor(17,27,22)
    motor.set_direction('FORWARD')
    while 1:

        for x in range(100):
            motor.set_speed(x)
            time.sleep(0.1)

        for x in range(100):
            motor.set_speed(100-x)
            time.sleep(0.1)

        motor.change_direction() 
finally:
    GPIO.cleanup()
