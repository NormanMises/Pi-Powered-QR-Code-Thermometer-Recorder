# 有源

import time

import RPi.GPIO as GPIO


class buzzer:
    def __init__(self, pin):
        self.BuzzerPin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.BuzzerPin, GPIO.OUT)
        GPIO.output(self.BuzzerPin, GPIO.LOW)

    def destroy(self):
        GPIO.output(self.BuzzerPin, GPIO.LOW)
        GPIO.cleanup()

    def alert(self, x):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.BuzzerPin, GPIO.OUT)
        # try:
        # while True:
        GPIO.output(self.BuzzerPin, GPIO.HIGH)
        time.sleep(x)

        GPIO.output(self.BuzzerPin, GPIO.LOW)
        time.sleep(x)

        GPIO.output(self.BuzzerPin, GPIO.HIGH)
        time.sleep(x)

        GPIO.output(self.BuzzerPin, GPIO.LOW)
        time.sleep(x)
    # except:
    #     destroy()
