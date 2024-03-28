import matplotlib.pyplot as plt
import numpy as np
import os
import re
from geopy.distance import geodesic # might need to change 

t = []
A = []
V = []
P = []

Velocity_m = []
GPS_data = []
cords = []
distance_change= []
lat_data, lng_data = [], []
save_directory = "graphs"

def main():
    read_data() # Gather data from text 
    calculate_power()
    calculate_velocity() # calculates and prints list of velocities
    average_lat_lng() # must be called after read_data()

    # Create graph
    graph_A()
    graph_V()
    graph_P()
    graph_Velo_m()
    plt.show() # include to view graphs simultaneously

def save_graph(directory, filename):
    create_directory(directory)
    full_path = os.path.join(directory, filename)
    plt.savefig(full_path)

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Parses data from data file and inserts into arrays to be used in this script
# Text file data is assumed to be tab seperated
def read_data(): # should return 4 lists all containing floats
    with open("data2.txt", 'r') as file:
        for line in file:
            data = re.split(r'\s+', line.strip())  # Splits at whitespace chars
            t.append(float(data[0]))
            A.append(float(data[1]))
            V.append(float(data[2]))
            if len(data) >= 4:  # Check if line contains lat/lng 
                if '=' in data[3]: # handles if lat/lng contains non float data   
                    cleaned_data = [item.split('=')[1] for item in data if '=' in item and 'and' not in item] 
                    coords = (float(cleaned_data[0]), float(cleaned_data[1]))
                    GPS_data.append(coords)
                else:
                    coords = (float(data[3]), float(data[4])) 
                    GPS_data.append(coords)

    #print(t)
    #print(A)
    #print(V)
    #print(P)
    #print(GPS_data)

def calculate_power():
    for index, item in enumerate(t):
        P.append(A[index]*V[index])  # P = i * v for eah time interval

# replaced process_GPS and calculate_velocity with singular function to calculate velocity 
def calculate_velocity(): # uses t and GPS_data to calc velocity
    for i in range(1, len(GPS_data)):
        distance_meters = geodesic(GPS_data[i-1], GPS_data[i]).meters  # Calculate distance between coords
        dt = t[i] - t[i-1]  # Change in time from previous sample point
        if dt > 0:
            velocity_round = round(distance_meters/dt,2)
            Velocity_m.append(velocity_round)  # Append velocity in mps 
        else:
            Velocity_m.append(0) 

    #print(Velocity_m) # currently prints list of velocities


def average_lat_lng():
    lat_data, lng_data = [], []
    for lat, lng in GPS_data:  # Iterate directly over each coordinate tuple
        lat_data.append(lat)
        lng_data.append(lng)
    avg_lat = sum(lat_data) / len(lat_data)
    avg_lng = sum(lng_data) / len(lng_data)
    print(f"Average Latitude is {avg_lat} and Average Longitude is {avg_lng}")

def graph_A():
    # Plot the data
    plt.plot(t, A, label='Amps (A)', linestyle='-')
    # Add labels and a legend
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.title('Current draw over time')
    plt.legend()
    plt.grid(True)
    save_graph(save_directory, "graph_A.png")
    #plt.close('all')

def graph_V():
    # Plot the data
    plt.plot(t, V, label='Voltage (V)', linestyle='-')
    # Add labels and a legend
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.title('Time vs Voltage')
    plt.legend()
    plt.grid(True)
    save_graph(save_directory, "graph_V.png")
    #plt.close('all')


def graph_Velo_m():
    t_mod = t[3::3]  # Adjusted time intervals to keep every third interval
    # print(t_mod)
    Velocity_mod = Velocity_m[:len(t_mod)]  # shouldn't be necessary, but will chop off additional velocity data points if needed
    #print(Velocity_mod)
    plt.plot(t_mod, Velocity_mod, label='Velocity (m/s)', linestyle='-')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Velocity over time')
    plt.legend()
    plt.grid(True)
    save_graph(save_directory, "graph_Velo_m.png")
    #plt.close('all')


def graph_P():
    # Plot the data
    plt.plot(t, P, label='Power (watts)',  linestyle='-')
    # Add labels and a legend
    plt.xlabel('Time (s)')
    plt.ylabel('Power (watts)')
    plt.title('Power over time')
    plt.legend()
    plt.grid(True)
    save_graph(save_directory, "graph_P.png")
    #plt.close('all')
    
if __name__ == "__main__":
    print("Creating Graphs")
    main()
    print("Done...")
    print("Graphs Created")

    