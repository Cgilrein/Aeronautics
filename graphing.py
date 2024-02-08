import matplotlib.pyplot as plt
import numpy as np
import os

t = []
A = []
V = []
P = []
Velocity_ft = []
Velocity_m = []
GPS_data = []
cords = []
distance_change= []
save_directory = "graphs"

def main():
    read_data() # Gather data from text 
    calculate_power()
    process_gps()
    calculate_velocity()

    # Create graph
    graph_A()
    graph_V()
    graph_P()
    graph_Velo_m()
    graph_Velo_ft()

def save_graph(directory, filename):
    create_directory(directory)
    full_path = os.path.join(directory, filename)
    plt.savefig(full_path)

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Parses data from data file and inserts into arrays to be used in this script
# Text file data is assumed to be tab seperated
def read_data():
    with open("data.txt", 'r') as file:
        for line in file:
            data = line.strip().split('\t')
            t.append(float(data[0]))
            A.append(float(data[1]))
            V.append(float(data[2]))
            GPS_data.append(float(data[3]))

def calculate_power():
    for index, item in enumerate(t):
        P.append(A[index]*V[index])  # P = i * v for eah time interval

def process_gps():
    previous_lat = None
    previous_long = None

    # Parsing GPS data
    for index, item in enumerate(GPS_data):
        # Insert cords into a list of (Lat,Long) formatted tuples
        cords.append(GPS_data.strip("i"),GPS_data.strip("i"))
    for index, coordinates in enumerate(cords):
        if index == 0:
            distance_change.append(0)
        else:
            change_y = (coordinates[0] - previous_lat) * 364000 # One degree lat = 364000 feet
            change_x = (coordinates[1] - previous_long) * 288200 # One degree long = 288200 feet
            # Use pythag. theorem to caclulate distance traveled
            total_change = np.sqrt((change_x^2) + (change_y^2))  # Total change in feet from last data point
            distance_change.append(total_change)
            # Set current cords to prev. for next calculation
            previous_lat, previous_long = coordinates[0], coordinates[1]

def calculate_velocity():
    for index, value in enumerate(t):
        if index == 0:
            Velocity_ft.append(0)
        else:
            dt = t[index] - t[index-1] # change in time from previous sample point
            Velocity_ft.append(distance_change/dt)
    for i in Velocity_ft:
        Velocity_m.append(i * 0.305) # Convert to meters

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
    plt.close('all')

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
    plt.close('all')


def graph_Velo_ft():
    # Plot the data
    plt.plot(t, Velocity_ft, label='Velocity (ft/s)',  linestyle='-')
    # Add labels and a legend
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (ft/s)')
    plt.title('Velocity over time')
    plt.legend()
    plt.grid(True)
    save_graph(save_directory, "graph_Velo_ft.png")
    plt.close('all')

def graph_Velo_m():
    # Plot the data
    plt.plot(t, Velocity_m, label='Velocity (m/s)',  linestyle='-')
    # Add labels and a legend
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Velocity over time')
    plt.legend()
    plt.grid(True)
    save_graph(save_directory, "graph_Velo_m.png")
    plt.close('all')

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
    plt.close('all')

if __name__ == "__main__":
    print("Creating Graphs")
    main()
    print("Done...")
    print("Graphs Created")
