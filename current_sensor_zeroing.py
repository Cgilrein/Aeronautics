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
    currents_value = []
    currents_voltage = []
    actual_current = input("Use multimeter to probe real world current, input value here: ")
    print("Test will run for 10 seconds... Starting in")
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    for loop in range(100):
        print("{:>5}\t{:>5.5f}".format(channel.value, (channel.voltage)))
        currents_value.append(channel.value)
        currents_voltage.append(channel.voltage)
        time.sleep(0.1)
    print("RESULTS")
    print("Actual current of "+str(actual_current) + "corresponds to")
    
    average_value = 0
    average_voltage = 0
    for loop, value in enumerate(currents_value):
        average_voltage += currents_voltage(loop) 
        average_value += currents_value(loop)

    average_value = average_value / len(currents_value)
    average_voltage = average_voltage / len(currents_voltage)

    print("A digital value of... "+ str(average_value))
    print("A voltage value of... " + str(average_voltage))