from time import sleep
from Adafruit_ADS1x15 import ADS1115

################ CONFIGS ##################################
samples_per_sec = 4
run_time = 600  # Requested runtime in seconds
amps_channel = 0  # ADC channel for the current sensor on ADS1115
volts_channel = 1  # ADC channel for the voltage sensor on ADS1115
###########################################################

time_array = []   # Time array
amps = []         # Amp array
volts = []        # Voltage array

sample_rate = 1 / samples_per_sec  # Sample rate in samples per second
data_file = 'data.txt'             # File to save and read data

ads = ADS1115()

with open(data_file, 'w') as file:
    pass  # This does nothing, but it effectively clears the file

def main():
    time = 0
    while time < (run_time * samples_per_sec):
        time_array.append(time)
        amps.append(get_amps())
        volts.append(get_voltage())
        time += sample_rate
        save_data()
        sleep(sample_rate)

def get_amps():
    try:
        print("Reading current sensor...")
        value = ads.read_adc(amps_channel, gain=1)
        voltage = value / 32767.0 * 4.096  # Assuming gain=1 and VDD=4.096V
        return round(voltage, 2)
    except:
        print("An error occurred while reading current sensor")
        return None

def get_voltage():
    try:
        print("Reading voltage sensor...")
        value = ads.read_adc(volts_channel, gain=1)
        voltage = value / 32767.0 * 4.096  # Assuming gain=1 and VDD=4.096V
        return round(voltage, 2)
    except:
        print("An error occurred while reading voltage sensor")
        return None

def save_data():
    with open(data_file, 'a') as file:
        latest_time = time_array[-1]
        latest_amp = amps[-1]
        latest_volt = volts[-1]
        file.write(f"{latest_time}\t{latest_amp}\t{latest_volt}\n")

if __name__ == "__main__":
    main()
    print("Telemetry Script Stopped Successfully")