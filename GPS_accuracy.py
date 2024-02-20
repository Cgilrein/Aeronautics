# must install geopy
import geopy.distance

# Input GPS coordinates for location A and B 
lat1 = float(input("Enter GPS latitude for location A: "))
lon1 = float(input("Enter GPS longitude for location A: "))
lat2 = float(input("Enter GPS latitude for location B: "))
lon2 = float(input("Enter GPS longitude for location B: "))

# Get the actual distance from Google Maps for comparison
actual_dist = float(input("Enter the actual distance between location A and B as determined by Google Maps: "))

coords_1 = (lat1, lon1)
coords_2 = (lat2, lon2)

dist = geopy.distance.geodesic(coords_1, coords_2).km
GPS_dist = round(dist * 1000, 2) 
error_distance =((actual_dist - GPS_dist) / actual_dist) * 100

print("GPS-determined distance between location A and B:", GPS_dist, "meters")
print("GPS distance is off by a margin of:", abs(error_distance), "%")
