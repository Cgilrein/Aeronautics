from time import sleep
from Adafruit_ADS1x15 import ADS1115

ads = ADS1115()

# Define the GPIO pin you want to re

volts_channel = 1  # ADC channel for the voltage sensor on ADS1115

def get_voltage():
    try:
        # Read the analog value from the specified channel
        value = ads.read_adc(volts_channel, gain=1)
        
        # Convert the raw ADC value to voltage (assuming 5V reference voltage)
        voltage = value * 0.000125  # 0.000125 V per unit for gain=1
        
        return voltage
    except Exception as e:
        print(f"An error occurred while reading voltage sensor: {e}")
        return None

while True:
    voltage_value = get_voltage()
    
    if voltage_value is not None:
        print(f"Voltage: {voltage_value:.2f} V")
    
    sleep(1)
