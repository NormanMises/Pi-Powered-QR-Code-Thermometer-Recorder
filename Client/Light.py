import RPi.GPIO as GPIO


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class Light():
    def __init__(self, R, G, B):
        self.R = R  # 11   G17
        self.G = G  # 36   G16
        self.B = B  # 33   G13
        self.pins = [self.R, self.G, self.B]

        GPIO.setmode(GPIO.BOARD)

        for i in self.pins:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)

        self.p_R = GPIO.PWM(self.R, 2000)
        self.p_G = GPIO.PWM(self.G, 2000)
        self.p_B = GPIO.PWM(self.B, 2000)

        self.p_R.start(0)  # 占空比是高电平持续时间和低电平持续时间之间的比例，决定亮度/速度
        self.p_G.start(0)
        self.p_B.start(0)

    def __del__(self):
        pass
        # self.destroy()

    def destroy(self):
        for i in self.pins:
            GPIO.output(i, GPIO.LOW)  # Turn off all leds
        # GPIO.cleanup()

    def setColor(self, col: int):  # For example : col = 0x112233
        col = int(col)
        R_val = (col & 0xff0000) >> 16
        G_val = (col & 0x00ff00) >> 8
        B_val = (col & 0x0000ff) >> 0

        R_val = map(R_val, 0, 255, 0, 100)
        G_val = map(G_val, 0, 255, 0, 100)
        B_val = map(B_val, 0, 255, 0, 100)

        self.p_R.ChangeDutyCycle(R_val)
        self.p_G.ChangeDutyCycle(G_val)
        self.p_B.ChangeDutyCycle(B_val)
