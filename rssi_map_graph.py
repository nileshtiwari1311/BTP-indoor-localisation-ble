import numpy as np 
from matplotlib import pyplot as plt 
import json
import os

ref_dir = os.getcwd() + "/beaconRef/"
f = open(os.path.join(ref_dir, "beaconRef.json"),"r")
data = json.load(f)
f.close()

save_dir = os.getcwd() + "/Graphs/rssi_map_discrete/"
if not(os.path.isdir(save_dir)) : 
	os.mkdir(save_dir)

b1 = {}

for it in data["beaconRef"]:
	x_coord = it["x-coord"]
	y_coord = it["y-coord"]
	ref_point = (x_coord, y_coord)
	beacon_rssi = {}
	for reading in it["beaconData"]:
		beacon_rssi[reading["id3"]] = reading["rssi"]
	b1[ref_point] = beacon_rssi

for beaconNo in range(1,7) :
	w, h = 60, 3;
	Matrix = [[np.NaN for x in range(w)] for y in range(h)]

	for i in range(1,60) :
		if i%2 == 0:
			ref_point = (i, 1)
			Matrix[0][i] = b1[ref_point][beaconNo]
			ref_point = (i, 5)
			Matrix[2][i] = b1[ref_point][beaconNo]
		else :
			ref_point = (i, 3)
			Matrix[1][i] = b1[ref_point][beaconNo]

	rssi_map = np.array(Matrix)
	plt.figure(figsize=(16, 10))
	plt.title("Signal strength map (discrete) of beacon " + str(beaconNo) + " located at (" + str(10*beaconNo-5) + ", " + str(0 if beaconNo%2==1 else 6) + ")\n")
	plt.imshow(rssi_map, cmap='hot', interpolation='nearest', extent=[1,60,6,0], aspect="0.5")
	plt.colorbar(orientation='horizontal')
	plt.clim(-100, -40)
	# plt.show()
	filename = os.path.join(save_dir, "rssi_map_" + str(beaconNo))
	plt.savefig(filename, dpi=200, bbox_inches='tight')
	plt.close()