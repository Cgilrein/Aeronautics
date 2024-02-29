import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import serial
from time import sleep, time
import datetime
import pynmea2
import os
import threading

################ CONFIGS ##################################

run_time = 600  # Requested runtime in seconds

################# Inititalize ADC ############################

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
ads.gain = 1

volts_channel = AnalogIn(ads, ADS.P0)
amps_channel = AnalogIn(ads, ADS.P1)

###########################################################

time_array = []  # Time array for circuit probing
amps = []        # Amp array
volts = []       # Voltage array
lat_array = []
lng_array =[]   # GPS coords arrays

# Get the current date and time
current_date = datetime.datetime.now().strftime('%Y-%m-%d')
current_time = datetime.datetime.now().strftime('%H-%M-%S')

# Define the directory name and file name for circuit data
circuit_data_directory = 'circuit_data'
circuit_data_filename = f"{current_date}__{current_time}__circuit_data.txt"
circuit_data_file = os.path.join(circuit_data_directory, circuit_data_filename)

# Define the directory name and file name for GPS data
gps_data_directory = 'gps_data'
gps_data_filename = f"{current_date}__{current_time}__gps_data.txt"
gps_data_file = os.path.join(gps_data_directory, gps_data_filename)

# Create the directories if they don't exist
for directory in [circuit_data_directory, gps_data_directory]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Create or clear the data files
for data_file in [circuit_data_file, gps_data_file]:
    with open(data_file, 'w') as file:
        pass  # This does nothing, but it effectively clears the file

def probe_circuit():
    start_time = time()  # Take start time based on computer time

    while (time() - start_time) < run_time:
        current_time = time() - start_time  # Get current time for circuit probing
        time_array.append(current_time)

        # Print Probing Values
        print("Time: {:.2f} seconds".format(current_time))
        print("Amps (Value, Actual): {}   {:.5f}".format(amps_channel.value, (amps_channel.voltage * -97.2 + 246)))
        print("Voltage (Value, Actual * 5): {}   {:.5f}".format(volts_channel.value, volts_channel.voltage * 5))
        print("\n")

        amps.append(amps_channel.voltage * -97.2 + 246)
        volts.append((volts_channel.voltage) * 5)
        save_circuit_data()
        sleep(0.01)  # Sleep for small time

def probe_gps():
    gps_time_array = []  # Time array for GPS probing
    start_time = time()
    
    while (time() - start_time) < run_time:
        try:
            ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
            dataout = pynmea2.NMEAStreamReader()
            newdata = ser.readline()
            gps_error = True
            if '$GPRMC' in str(newdata):
                newmsg = pynmea2.parse(newdata.decode('utf-8'))
                lat = newmsg.latitude
                lng = newmsg.longitude
                lat_array.append(lat)
                lng_array.append(lng)

                gps = "Latitude={} and Longitude={}".format(lat, lng)
                gps_error = False
                print(gps) # Prints lat/lng info continuously
                
                # Record GPS time
                gps_time_array.append(time() - start_time)
        except:
            print("Error Retrieving GPS")

        save_gps_data(gps_error, gps_time_array)
        sleep(0.1)  # Sleep for small time

def save_circuit_data():
    with open(circuit_data_file, 'a') as file:
        latest_time = time_array[-1]
        latest_amp = amps[-1]
        latest_volt = volts[-1]
        file.write(f"{latest_time:.2f}\t{latest_amp}\t{latest_volt}\n")

def save_gps_data(gps_error, gps_time_array):
    with open(gps_data_file, 'a') as file:
        try:
            latest_lat = lat_array[-1]
            latest_lng = lng_array[-1]
        except IndexError:
            latest_lat = latest_lng = ""
        if gps_error:
            file.write(f"GPS Error\n")
        else:
            for i in range(len(gps_time_array)):
                file.write(f"{gps_time_array[i]:.2f}\t{latest_lat}\t{latest_lng}\n")

if __name__ == "__main__":
    print("Telemetry Script Began")

    # Start the circuit probing thread
    circuit_thread = threading.Thread(target=probe_circuit)
    circuit_thread.start()

    # Start the GPS probing thread
    gps_thread = threading.Thread(target=probe_gps)
    gps_thread.start()

    # Wait for both threads to finish
    circuit_thread.join()
    gps_thread.join()

    print("Telemetry Script Stopped Successfully")