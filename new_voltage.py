import time
import board
import busio
from Adafruit_ADS1x15 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.D1, board.D0)

ads = ADS1115(i2c)
ads.gain = 1

channel = AnalogIn(ads, ADS1115.P0)

print("{:>5}\t{:>5}".format("raw","v"))

while True:
    print("{:>5}\t{:>5.5f}".format(channel.value, channel.voltage))
    time.sleep(0.5)
