import numpy as np 
from matplotlib import pyplot as plt 
import json
import os

filterMethod = "raw"

parameter_dir = os.getcwd() + "/Path-Loss-Model/"
f = open(os.path.join(parameter_dir, "path_loss_parameters.json"), "r")
data = json.load(f)
f.close()

noOfBeacons = 10
#  beacons ka position
xi = [18,26,0,14,0,14,38,26,18,38]
yi = [18,38,26,38,14,0,14,0,20,26]

ai = [0 for i in range(noOfBeacons)]
bi = [0 for i in range(noOfBeacons)]

for it in data["model"]["parameters"] :
	id3 = it["id3"]
	ai[id3-1] = it["a"]
	bi[id3-1] = it["b"]

data_dir = os.getcwd() + "/beacon-all-points-" + filterMethod + "/"
f = open(os.path.join(data_dir, "beacon.json"),"r")
data = json.load(f)
f.close()

save_path = os.getcwd() + "/Graphs/rssi_map_continuous/"
if not(os.path.isdir(save_path)) : 
	os.mkdir(save_path)

noOfTilesX = 19
noOfTilesY = 19
beacon_data = {}

scaleX = 0.3
scaleY = 0.3

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
		Matrix[data_point[0]//2][data_point[1]//2] = beacon_data[data_point][beaconNo]

	for i in range(h) :
		for j in range(w) :
			if np.isnan(Matrix[i][j]) :
				x_coord = i*2 + 1
				y_coord = j*2 + 1
				distance = (((x_coord-xi[beaconNo-1])*scaleX)**2 + ((y_coord-yi[beaconNo-1])*scaleY)**2)**(0.5)
				distance = round(distance, 2)
				rssi_new = ai[beaconNo-1] + bi[beaconNo-1]*np.log10(distance)
				Matrix[i][j] = rssi_new

	rssi_map = np.array(Matrix)
	plt.figure(figsize=(16, 10))
	# plt.title("Signal strength map (discrete) of beacon " + str(beaconNo) + "\n")
	# plt.yticks([i for i in range(1, h+1)])
	# plt.xticks([i for i in range(1, w+1)])
	plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
	plt.tick_params(axis='x', which='both', bottom=False, top=False, left=False, labelbottom=False)
	plt.imshow(rssi_map, cmap='hot', interpolation='nearest', extent=[0,w,h,0])
	plt.colorbar(orientation='horizontal')
	plt.clim(-100, -40)
	# plt.show()
	filename = os.path.join(save_path, "rssi_map_" + str(beaconNo))
	plt.savefig(filename, dpi=200, bbox_inches='tight')
	plt.close()