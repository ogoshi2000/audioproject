
import time
import board
import busio
import adafruit_pca9685
import sys

i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)

hat.frequency = int(sys.argv[1])
led_channel = hat.channels[0]
cycle = int(sys.argv[2])**2

led_channel.duty_cycle = cycle/2

while True:
    pass
