from time import sleep
from Adafruit_ADS1x15 import ADS1115

ads = ADS1115()

# Define the GPIO pin you want to re

volts_channel = 1  # ADC channel for the voltage sensor on ADS1115

def get_voltage():
    try:
        print("Reading voltage sensor...")
        value = ads.read_adc(volts_channel, gain=1)
        voltage = value / 32767.0 * 4.096  # Assuming gain=1 and VDD=4.096V
        return round(voltage, 2)
    except:
        print("An error occurred while reading voltage sensor")
        return None


while True:
    value = get_voltage()
    print(value)
    sleep(1)
