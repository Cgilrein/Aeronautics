import numpy as np
import matplotlib.pyplot as plt
import re
from geopy.distance import geodesic
import time

# Init global variables 
t_circuit = []
a = []
v = []
power = []


def read_data(): 
    with open("./circuit_data/2024-04-02__18-06-49__circuit_data.txt", 'r') as f1: # hard code appropriate file names 
        for line in f1:
            data = re.split(r'\s+', line.strip())  # Splits at whitespace chars
            t_circuit.append(float(data[0]))    
            a.append(float(data[1]))
            v.append(float(data[2]))


def plot_position():
    meters_traveled = [0.0]  # Initialize with zero for the first data point
    time_array = [0.0]
    data = np.loadtxt("./gps_data/2024-04-02__18-06-44__gps_data.txt")
    # Filter out data points with latitude and longitude values of 0.0
    valid_data_indices = np.where((data[:, 1] != 0.0) & (data[:, 2] != 0.0))
    data = data[valid_data_indices]
    # Extract time_array, latitude, and longitude from the data
    time_array_np = data[:, 0]
    lat = data[:, 1]
    lng = data[:, 2]

    # calculates net distance travelled using lat_lng and t_gps
    for i in range(1, len(time_array_np)):
        # Check if there are enough GPS coordinates available
        distance = geodesic((lat[i-1], lng[i-1]), (lat[i], lng[i])).meters
        meters_traveled.append(meters_traveled[-1] + distance)
        time_array.append(time_array_np[i])
    plt.plot(time_array, meters_traveled, label='Meters Traveled')
    plt.xlabel('Time')
    plt.ylabel('Meters Traveled')
    plt.title('Net Meters Traveled vs Time')
    plt.legend()
    plt.show()


def plot_amps():
    plt.plot(t_circuit, a, label='Amps', marker='o', color='red')
    plt.xlabel('Time')
    plt.ylabel('Amperage')
    plt.title('Amperage vs Time')
    plt.legend()
    plt.show()


def plot_volts():
    plt.plot(t_circuit, v, label='Volts', marker='o', color='red')
    plt.xlabel('Time')
    plt.ylabel('Volts')
    plt.title('Volts vs Time')
    plt.legend()
    plt.show()


def plot_power():
    for i in range(len(a)):
        power_val = round(a[i] * v[i], 2)
        power.append(power_val)
    plt.plot(t_circuit, power, label='Power (W)', marker='o', color='red')
    plt.xlabel('Time')
    plt.ylabel('Power (W)')
    plt.title('Power vs Time')
    plt.legend()
    plt.show()


def plot_velocity():
    data = np.loadtxt("./gps_data/2024-04-02__18-06-44__gps_data.txt")

    # Filter out data points with latitude and longitude values of 0.0
    valid_data_indices = np.where((data[:, 1] != 0.0) & (data[:, 2] != 0.0))
    data = data[valid_data_indices]

    # Extract time_array, latitude, and longitude from the data
    time_array = data[:, 0]
    lat = data[:, 1]
    lng = data[:, 2]

    # Calculate speed in mph
    velocity = []
    for i in range(1, len(time_array)):
        time_diff = time_array[i] - time_array[i-1]  # In seconds
        distance_km = geodesic((lat[i-1], lng[i-1]), (lat[i], lng[i])).km
        speed_km_s = distance_km / time_diff  # in km/s
        speed_km_h = speed_km_s * 3600     # convert to km/h
        
        speed_miles_hour = speed_km_h * 0.621371

        velocity.append(speed_miles_hour)

    plt.plot(time_array[1:], velocity, label='Velocity', color='green')
    plt.xlabel('Time')
    plt.ylabel('Velocity (Miles per hour)')
    plt.title('Velocity vs Time')
    plt.legend()
    plt.show()


def main():
    read_data()
    plot_position()
    plot_amps()
    plot_volts()
    plot_velocity() #uncomment this if you want velocity vs time graph
    plot_power()

if __name__ == "__main__":
    main()
