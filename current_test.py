import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
ads.gain = 1

channel = AnalogIn(ads, ADS.P1)

print("{:>5}\t{:>5}".format("raw","i"))

while True:
    temp = []
    for i in range(10):
        temp.append(channel.voltage * -97.2 + 246)
        time.sleep(0.05)
    print(max(temp))
    #print("{:>5}\t{:>5.5f}".format(channel.value, (channel.voltage * -97.2 + 246)))
    
