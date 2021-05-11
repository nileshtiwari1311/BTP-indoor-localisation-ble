import numpy as np 
from matplotlib import pyplot as plt 
import json
import os

filterMethod = "kalman"

data_dir = os.getcwd() + "/beacon-all-points-" + filterMethod + "/"
f = open(os.path.join(data_dir, "beacon.json"),"r")
data = json.load(f)
f.close()

save_path = os.getcwd() + "/Graphs/rssi_map_discrete/"
if not(os.path.isdir(save_path)) : 
	os.mkdir(save_path)

noOfBeacons = 10
noOfTilesX = 14
noOfTilesY = 20
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
	w, h = noOfTilesY, noOfTilesX;
	Matrix = [[np.NaN for x in range(w)] for y in range(h)]

	for data_point in beacon_data :
		Matrix[data_point[0]//2][(data_point[1]-1)//2] = beacon_data[data_point][beaconNo]

	rssi_map = np.array(Matrix)
	plt.figure(figsize=(16, 10))
	plt.title("Signal strength map (discrete) of beacon " + str(beaconNo) + "\n")
	plt.yticks([i for i in range(1, h+1)])
	plt.xticks([i for i in range(1, w+1)])
	plt.imshow(rssi_map, cmap='hot', interpolation='nearest', extent=[0,w,h,0])
	plt.colorbar(orientation='horizontal')
	plt.clim(-100, -40)
	# plt.show()
	filename = os.path.join(save_path, "rssi_map_" + str(beaconNo))
	plt.savefig(filename, dpi=200, bbox_inches='tight')
	plt.close()