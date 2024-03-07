import numpy as np
import matplotlib.pyplot as plt
import re
from geopy.distance import geodesic

# Init global variables 
t_gps = []
t_circuit = []
a = []
v = []
lat_lng = [] # list of tuple coordinates 
lat, lng = [], []
power = []


def read_data(): 
    with open("sample_circuit_data.txt", 'r') as f1: # hard code appropriate file names 
        for line in f1:
            data = re.split(r'\s+', line.strip())  # Splits at whitespace chars
            t_circuit.append(float(data[0]))    
            a.append(float(data[1]))
            v.append(float(data[2]))
    with open("sample_gps_data.txt", 'r') as f2:
        for line in f2:
            try: 
                data = re.split(r'\s+', line.strip())  
                if data[1] and data[2]: # appends appropriate lists if long/lat data is available
                    t_gps.append(float(data[0]))
                    lat_lng.append((float(data[1]), float(data[2])))
            except IndexError: # skips line if there is no lat/lng data so not to mess up indexing 
                pass


def plot_position():
    meters_traveled = [0.0]  # Initialize with zero for the first data point
    for coord in lat_lng:
        lat.append(coord[0])
        lng.append(coord[1])
    # calculates net distance travelled using lat_lng and t_gps
    for i in range(1, len(lat_lng)):
        distance = geodesic((lat[i-1], lng[i-1]), (lat[i], lng[i])).meters
        meters_traveled.append(meters_traveled[-1] + distance)

    plt.plot(t_gps, meters_traveled, label='Meters Traveled', marker='o')
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
    for current_val, volt_val in a, v:
        power_val = round(current_val * volt_val, 2)
        power.append(power_val)
    print(power)


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
    velocity = [0.0]  
    for i in range(1, len(lat_lng)):
        distance = geodesic((lat[i-1], lng[i-1]), (lat[i], lng[i])).meters
        time_diff = t_gps[i] - t_gps[i-1]
        # dist=velocity/time_diff!!
        if time_diff != 0:
            velocity.append(distance / time_diff)
        else:
            velocity.append(0.0)

    plt.plot(t_gps, velocity, label='Velocity', marker='o', color='green')
    plt.xlabel('Time')
    plt.ylabel('Velocity (m/s)')
    plt.title('Velocity vs Time')
    plt.legend()
    plt.show()


def main():
    read_data()
    plot_position()
    plot_amps()
    plot_volts()
    #plot_velocity() #uncomment this if you want velocity vs time graph
    plot_power()

if __name__ == "__main__":
    main()
