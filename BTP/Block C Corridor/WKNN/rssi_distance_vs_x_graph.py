import json
import os
from matplotlib import pyplot as plt 

noOfBeacons = 6
noOfTilesX = 60

filterMethod = "raw"

beacon_rssi_dict = {}
beacon_distance_dict = {}
data_dir = os.getcwd() + "/beacon-all-points-" + filterMethod + "/"
f = open(os.path.join(data_dir, "beacon.json"),"r")
data = json.load(f)
f.close()

save_path_rssi = os.getcwd() + "/Graphs/rssi_vs_x/"
if not(os.path.isdir(save_path_rssi)) : 
	os.mkdir(save_path_rssi)

save_path_distance = os.getcwd() + "/Graphs/distance_vs_x/"
if not(os.path.isdir(save_path_distance)) : 
	os.mkdir(save_path_distance)

for it in data["beacon"]:
	x_coord = it["x-coord"]
	y_coord = it["y-coord"]
	data_point = (x_coord, y_coord)
	beacon_rssi = {}
	beacon_distance = {}
	for reading in it["beaconData"]:
		beacon_rssi[reading["id3"]] = reading["rssi"]
		beacon_distance[reading["id3"]] = reading["distance"]
	beacon_rssi_dict[data_point] = beacon_rssi
	beacon_distance_dict[data_point] = beacon_distance

x_list_1 = [[] for x in range(noOfBeacons)]
x_list_3 = [[] for x in range(noOfBeacons)]
x_list_5 = [[] for x in range(noOfBeacons)]
rssi_list_1 = [[] for x in range(noOfBeacons)]
rssi_list_3 = [[] for x in range(noOfBeacons)]
rssi_list_5 = [[] for x in range(noOfBeacons)]
distance_list_1 = [[] for x in range(noOfBeacons)]
distance_list_3 = [[] for x in range(noOfBeacons)]
distance_list_5 = [[] for x in range(noOfBeacons)]

for i in range(1, noOfTilesX) :
	if i%2 == 0:
		data_point = (i, 1)
		for j in range(1, noOfBeacons+1):
			if j in beacon_rssi_dict[data_point] :
				x_list_1[j-1].append(i)
				rssi_list_1[j-1].append(beacon_rssi_dict[data_point][j])
				distance_list_1[j-1].append(beacon_distance_dict[data_point][j])
		data_point = (i, 5)
		for j in range(1, noOfBeacons+1):
			if j in beacon_rssi_dict[data_point] :
				x_list_5[j-1].append(i)
				rssi_list_5[j-1].append(beacon_rssi_dict[data_point][j])
				distance_list_5[j-1].append(beacon_distance_dict[data_point][j])
	else :
		data_point = (i, 3)
		for j in range(1, noOfBeacons+1):
			if j in beacon_rssi_dict[data_point] :
				x_list_3[j-1].append(i)
				rssi_list_3[j-1].append(beacon_rssi_dict[data_point][j])
				distance_list_3[j-1].append(beacon_distance_dict[data_point][j])

for beaconNo in range(1, noOfBeacons+1):
	plt.figure(figsize=(16, 10))
	plt.title("Variation in RSSI with x coordinate for beacon " + str(beaconNo) + " located at (" + str(10*beaconNo-5) + ", " + str(0 if beaconNo%2 == 1 else 6) + ")") 
	plt.xlabel("X coordinates (1 unit = 0.6 metres)") 
	plt.ylabel("RSSI in dBm")
	plt.plot(x_list_1[beaconNo-1], rssi_list_1[beaconNo-1], "-ob")
	plt.plot(x_list_3[beaconNo-1], rssi_list_3[beaconNo-1], "-or")
	plt.plot(x_list_5[beaconNo-1], rssi_list_5[beaconNo-1], "-og")
	plt.axvline(x=10*beaconNo-5, color="black", linestyle="--")
	plt.legend(["Y coordinate = 1", "Y coordinate = 3", "Y coordinate = 5"])
	plt.grid()
	# plt.show()
	filename = os.path.join(save_path_rssi, "rssi_vs_x_" + str(beaconNo))
	plt.savefig(filename, dpi=200, bbox_inches='tight')
	plt.close()

	plt.figure(figsize=(16, 10))
	plt.title("Variation in reported distance from beacon with x coordinate for beacon " + str(beaconNo) + " located at (" + str(10*beaconNo-5) + ", " + str(0 if beaconNo%2 == 1 else 6) + ")")  
	plt.xlabel("X coordinates (1 unit = 0.6 metres)") 
	plt.ylabel("Distance in metres")
	plt.plot(x_list_1[beaconNo-1], distance_list_1[beaconNo-1], "-ob")
	plt.plot(x_list_3[beaconNo-1], distance_list_3[beaconNo-1], "-or")
	plt.plot(x_list_5[beaconNo-1], distance_list_5[beaconNo-1], "-og")
	plt.legend(["Y coordinate = 1", "Y coordinate = 3", "Y coordinate = 5"])
	plt.axvline(x=10*beaconNo-5, color="black", linestyle="--")
	plt.grid()
	# plt.show()
	filename = os.path.join(save_path_distance, "distance_vs_x_" + str(beaconNo))
	plt.savefig(filename, dpi=200, bbox_inches='tight')
	plt.close()