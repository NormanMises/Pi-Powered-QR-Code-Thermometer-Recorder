# 超声波
import time

import RPi.GPIO as GPIO


def destroy():
    pass
    # GPIO.cleanup()


class Sensor_ultrasonic():
    def __init__(self, ECHO, TRIG):
        # threading.Thread.__init__(self)
        self.ECHO = ECHO  # 12   
        self.TRIG = TRIG  # 11   
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.setup(self.TRIG, GPIO.OUT)

    def __del__(self):
        destroy()

    def distance(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.output(self.TRIG, 0)
        time.sleep(0.000002)

        GPIO.output(self.TRIG, 1)
        time.sleep(0.00001)

        GPIO.output(self.TRIG, 0)

        while GPIO.input(self.ECHO) == 0:
            pass
        st = time.time()

        while GPIO.input(self.ECHO) == 1:
            pass
        ed = time.time()

        during = ed - st

        return during * 340 / 2 * 100
