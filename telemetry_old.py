import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import serial
from time import sleep, time
import datetime
#import string
import pynmea2
import os

################ CONFIGS ##################################

run_time = 600  # Requested runtime in seconds
#minute_interval = 60  # Interval for calculating lat/lng averages 

################# Inititalize ADC ############################

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
ads.gain = 1

volts_channel = AnalogIn(ads, ADS.P0)
amps_channel = AnalogIn(ads, ADS.P1)

###########################################################

time_array = []  # Time array
amps = []        # Amp array
volts = []       # Voltage array
lat_array = []
lng_array =[]   # GPS coords arrays

# Get the current date and time
current_date = datetime.datetime.now().strftime('%Y-%m-%d')
current_time = datetime.datetime.now().strftime('%H-%M-%S')

# Define the directory name and file name
directory_name = 'data'
filename = f"{current_date}__{current_time}__data.txt"
data_file = os.path.join(directory_name, filename)

# Create the directory if it doesn't exist
if not os.path.exists(directory_name):
    os.makedirs(directory_name)

# Create or clear the data file
with open(data_file, 'w') as file:
    pass  # This does nothing, but it effectively clears the file

def main():
    start_time = time()  # Take start time based on computer time
    last_minute_start = start_time # Keeps track of most recent minute
    minute_count = 0 # Initializes minutes count

    while (time() - start_time) < run_time:
        current_time = time() - start_time  # Get current time
        time_array.append(current_time)

        # Print Probing Values
        print("Time: {:.2f} seconds".format(current_time))
        print("Amps (Value, Actual): {}   {:.5f}".format(amps_channel.value, (amps_channel.voltage * 0.0128 + 2.55)))
        print("Voltage (Value, Actual * 5): {}   {:.5f}".format(volts_channel.value, volts_channel.voltage * 5))
        print("\n")

        ######## GPS Section #####################
        ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
        dataout = pynmea2.NMEAStreamReader()
        newdata = ser.readline()
        gps_error = True
        if '$GPRMC' in str(newdata):
            gps_error = False
            #print(newdata.decode('utf-8'))
            newmsg = pynmea2.parse(newdata.decode('utf-8'))  
            lat = newmsg.latitude 
            lng = newmsg.longitude 
            lat_array.append(lat)
            lng_array.append(lng)

            gps = "Latitude={} and Longitude={}".format(lat, lng)
            print(gps) # Prints lat/lng info continuously
            
            # Check if a minute has passed since the last avg lat/lng calculation
            """if current_time - last_minute_start >= minute_interval:
                # Calculate and print avgs if lat/lng lists contain data 
                if lat_list:
                    avg_lat = sum(lat_list) / len(lat_list)
                    avg_lng = sum(lng_list) / len(lng_list)
                    print(f"Minute {minute_count + 1}: Average Latitude: {avg_lat:.6f}, Average Longitude: {avg_lng:.6f}")

                # Reset lists for the next minute
                
                reset = True
                minute_count += 1
                last_minute_start = current_time

            else:
                # Store lat/lng data for later averaging
                lat_list.append(lat)
                lng_list.append(lng)"""

        ########## END GPS ########################

        amps.append((amps_channel.voltage * 0.0128 + 2.55)) 
        volts.append((volts_channel.voltage) * 5)
        save_data(gps_error)
        sleep(0.1)  # Sleep for small time

def save_data(gps_error):
    with open(data_file, 'a') as file:
        latest_time = time_array[-1]
        latest_amp = amps[-1]
        latest_volt = volts[-1]
        try:
            latest_lat = lat_array[-1]
            latest_lng = lng_array[-1]
        except:
            pass
        if gps_error:
            file.write(f"{latest_time:.2f}\t{latest_amp}\t{latest_volt}\n")
        else:
            file.write(f"{latest_time:.2f}\t{latest_amp}\t{latest_volt}\t{latest_lat}\t{latest_lng}\n")

if __name__ == "__main__":
    print("Telemetry Script Began")
    main()
    print("Telemetry Script Stopped Successfully")
