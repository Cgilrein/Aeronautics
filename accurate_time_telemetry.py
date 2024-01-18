import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import serial
from time import sleep, time
import string
import pynmea2  

################ CONFIGS ##################################

samples_per_sec = 4
run_time = 600  # Requested runtime in seconds

################# Inititalize ADC ############################

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
ads.gain = 1

volts_channel = AnalogIn(ads, ADS.P0)
amps_channel = AnalogIn(ads, ADS.P1)

###########################################################

time_array = []   # Time array
amps = []         # Amp array
volts = []        # Voltage array
gps_array = []    # GPS coords array

sample_rate = 1 / samples_per_sec  # Sample rate in samples per second
data_file = 'data.txt'             # File to save and read data

with open(data_file, 'w') as file:
    pass  # This does nothing, but it effectively clears the file

def main():
    start_time = time()
    while (time() - start_time) < run_time:
        current_time = time() - start_time
        time_array.append(current_time)

        # Print Probing Values
        print("Time: {:.2f} seconds".format(current_time))
        print("Amps (Value, Actual): {}   {:.5f}".format(amps_channel.value, amps_channel.voltage - 2.59))
        print("Voltage (Value, Actual * 5): {}   {:.5f}".format(volts_channel.value, volts_channel.voltage * 5))
        print("\n")

        ######## GPS Section #####################
        ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
        dataout = pynmea2.NMEAStreamReader() 
        newdata = ser.readline()
        print("GPS raw data: ", end="")
        print(newdata)
        gps_error = True
        if '$GPRMC' in str(newdata):
            gps_error = False
            print(newdata.decode('utf-8'))
            newmsg = pynmea2.parse(newdata.decode('utf-8'))  
            lat = newmsg.latitude 
            lng = newmsg.longitude 
            gps = "Latitude={} and Longitude={}".format(lat, lng)
            gps_array.append(gps)
            print(gps)
        ########## END GPS ########################
            
        amps.append(amps_channel.value * -10) 
        volts.append((volts_channel.voltage) * 5)
        save_data(gps_error)
        sleep(sample_rate)

def save_data(gps_error):
    with open(data_file, 'a') as file:
        latest_time = time_array[-1]
        latest_amp = amps[-1]
        latest_volt = volts[-1]
        try:
            latest_gps = gps_array[-1]
        except:
            pass
        if gps_error:
            file.write(f"{latest_time:.2f}\t{latest_amp}\t{latest_volt}\n")
        else:
            file.write(f"{latest_time:.2f}\t{latest_amp}\t{latest_volt}\t{latest_gps}\n")

if __name__ == "__main__":
    print("Telemetry Script Began")
    main()
    print("Telemetry Script Stopped Successfully")