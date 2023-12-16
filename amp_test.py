from time import sleep
from Adafruit_ADS1x15 import ADS1115

ads = ADS1115()

# Define the GPIO pin you want to re

amps_channel = 0  # ADC channel for the voltage sensor on ADS1115

def get_current():
    try:
        print("Reading current sensor...")
        value = ads.read_adc(amps_channel, gain=1)
        amps = value / 32767.0 * 4.096  # Assuming gain=1 and VDD=4.096V
        return round(amps, 2)
    except:
        print("An error occurred while reading current sensor")
        return None


while True:
    value = get_current()
    print(value)
    sleep(1)