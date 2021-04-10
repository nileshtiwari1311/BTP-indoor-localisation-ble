import numpy as np 
from matplotlib import pyplot as plt 
import json
import os

filterMethod = "raw"

data_dir = os.getcwd() + "/beacon-all-points-" + filterMethod + "/"
f = open(os.path.join(data_dir, "beacon.json"),"r")
data = json.load(f)
f.close()

save_path = os.getcwd() + "/Graphs/rssi_map_discrete/"
if not(os.path.isdir(save_path)) : 
	os.mkdir(save_path)

noOfBeacons = 6
noOfTilesX = 60
noOfTilesY = 3
beacon_data = {}

for it in data["beacon"]:
	x_coord = it["x-coord"]
	y_coord = it["y-coord"]
	data_point = (x_coord, y_coord)
	beacon_rssi = {}
	for reading in it["beaconData"]:
		beacon_rssi[reading["id3"]] = reading["rssi"]
	beacon_data[data_point] = beacon_rssi

for beaconNo in range(1, noOfBeacons+1) :
	w, h = noOfTilesX, noOfTilesY;
	Matrix = [[np.NaN for x in range(w)] for y in range(h)]

	for data_point in beacon_data :
		Matrix[data_point[1]//2][data_point[0]] = beacon_data[data_point][beaconNo]

	rssi_map = np.array(Matrix)
	plt.figure(figsize=(16, 10))
	plt.title("Signal strength map (discrete) of beacon " + str(beaconNo) + " located at (" + str(10*beaconNo-5) + ", " + str(0 if beaconNo%2==1 else 3) + ")\n")
	plt.yticks([i for i in range(1, h+1)])
	plt.xticks([i for i in range(1, w+1)], rotation=60)
	plt.imshow(rssi_map, cmap='hot', interpolation='nearest', extent=[0,w,h,0])
	plt.colorbar(orientation='horizontal')
	plt.clim(-100, -40)
	# plt.show()
	filename = os.path.join(save_path, "rssi_map_" + str(beaconNo))
	plt.savefig(filename, dpi=200, bbox_inches='tight')
	plt.close()