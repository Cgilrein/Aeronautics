import matplotlib.pyplot as plt
import numpy as np

# Function to calculate distance between two points using Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers

    # Convert latitude and longitude from degrees to radians
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = R * c
    return distance

# Load data from file
data = np.loadtxt("./gps_data/2024-04-02__18-06-44__gps_data.txt")

# Filter out data points with latitude and longitude values of 0.0
valid_data_indices = np.where((data[:, 1] != 0.0) & (data[:, 2] != 0.0))
data = data[valid_data_indices]

# Extract time, latitude, and longitude from the data
time = data[:, 0]
latitudes = data[:, 1]
longitudes = data[:, 2]

# Calculate speed in mph
speeds = []
for i in range(1, len(time)):
    time_diff = time[i] - time[i-1]  # in hours
    distance = haversine(latitudes[i-1], longitudes[i-1], latitudes[i], longitudes[i])  # in kilometers
    speed_kmh = distance / time_diff  # in km/h
    speed_mph = speed_kmh * 0.621371  # convert to mph
    speeds.append(speed_mph * 3000) # The 3000 is a random constant I used to make the numbers make sense cus I got no clue why the mph is 1/3000 of what its supposed to be

# Plot speed
plt.plot(time[1:], speeds)
plt.xlabel("Time")
plt.ylabel("Instantaneous Speed (mph)")
plt.title("Instantaneous Speed vs. Time")
plt.grid(True)
plt.show()