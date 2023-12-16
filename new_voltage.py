import time
import smbus
from Adafruit_ADS1x15 import ADS1115

# Create an I2C bus
i2c = smbus.SMBus(1)

ads = ADS1115(i2c)
ads.gain = 1

channel = AnalogIn(ads, ADS1115.P0)

print("{:>5}\t{:>5}".format("raw","v"))

while True:
    print("{:>5}\t{:>5.5f}".format(channel.value, channel.voltage))
    time.sleep(0.5)
