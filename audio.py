
import time
import board
import busio
import adafruit_pca9685
import sys

i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)

hat.frequency = sys.argv[0]
led_channel = hat.channels[0]

led_channel.duty_cycle = (sys.argv[1]**2)/2

while true:
    pass

