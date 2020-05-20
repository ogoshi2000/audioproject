
import time
import board
import busio
import adafruit_pca9685
import sys
import time

i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)

hat.frequency = 1500
led_channel = hat.channels[0]
cycle = int(sys.argv[2])**2

led_channel.duty_cycle = 0

while True:
    for i in range(255):
        led_channel.duty_cycle = i
        time.sleep(10/1000)
    for i in range(255, 0, -1):
        led_channel.duty_cycle = i
        time.sleep(10/1000)
