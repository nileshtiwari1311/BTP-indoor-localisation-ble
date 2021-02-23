from matplotlib import pyplot as plt 
import json
import os

ref_dir = os.getcwd() + "/beaconRef/"
f = open(os.path.join(ref_dir, "beaconRef.json"),"r")
data = json.load(f)
f.close()

distance = {}
rssi = {}

for elem in data["beaconRef"]:
	for values in elem["beaconData"]:
		if values["id3"] in distance :
			distance[values["id3"]].append(values["distance"])
		else :
			distance[values["id3"]] = [values["distance"]]

		if values["id3"] in rssi :
			rssi[values["id3"]].append(values["rssi"])
		else :
			rssi[values["id3"]] = [values["rssi"]]
		

plt.title("Variation in RSSI received vs distance from Bluetooth beacon ") 
plt.xlabel("Distance in meters") 
plt.ylabel("RSSI in dBm") 
plt.plot(distance[1], rssi[1], "ob")  
plt.show()