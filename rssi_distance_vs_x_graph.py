import json
import os
from matplotlib import pyplot as plt 

b1 = {}
b2 = {}
ref_dir = os.getcwd() + "/beaconRef/"
f = open(os.path.join(ref_dir, "beaconRef.json"),"r")
data = json.load(f)
f.close()

for it in data["beaconRef"]:
	x_coord = it["x-coord"]
	y_coord = it["y-coord"]
	ref_point = (x_coord, y_coord)
	beacon_rssi = {}
	beacon_distance = {}
	for reading in it["beaconData"]:
		beacon_rssi[reading["id3"]] = reading["rssi"]
		beacon_distance[reading["id3"]] = reading["distance"]
	b1[ref_point] = beacon_rssi
	b2[ref_point] = beacon_distance

x_list_1 = [[] for x in range(6)]
x_list_3 = [[] for x in range(6)]
x_list_5 = [[] for x in range(6)]
rssi_list_1 = [[] for x in range(6)]
rssi_list_3 = [[] for x in range(6)]
rssi_list_5 = [[] for x in range(6)]
distance_list_1 = [[] for x in range(6)]
distance_list_3 = [[] for x in range(6)]
distance_list_5 = [[] for x in range(6)]

for i in range(1, 60) :
	if i%2 == 0:
		ref_point = (i, 1)
		for j in range(1, 7):
			if j in b1[ref_point] :
				x_list_1[j-1].append(i)
				rssi_list_1[j-1].append(b1[ref_point][j])
				distance_list_1[j-1].append(b2[ref_point][j])
		ref_point = (i, 5)
		for j in range(1, 7):
			if j in b1[ref_point] :
				x_list_5[j-1].append(i)
				rssi_list_5[j-1].append(b1[ref_point][j])
				distance_list_5[j-1].append(b2[ref_point][j])
	else :
		ref_point = (i, 3)
		for j in range(1, 7):
			if j in b1[ref_point] :
				x_list_3[j-1].append(i)
				rssi_list_3[j-1].append(b1[ref_point][j])
				distance_list_3[j-1].append(b2[ref_point][j])

beaconNo = 1

plt.plot(x_list_1[beaconNo-1], rssi_list_1[beaconNo-1], "-ob")
plt.show()

plt.plot(x_list_3[beaconNo-1], rssi_list_3[beaconNo-1], "-ob")
plt.show()

plt.plot(x_list_5[beaconNo-1], rssi_list_5[beaconNo-1], "-ob")
plt.show()

plt.plot(x_list_1[beaconNo-1], distance_list_1[beaconNo-1], "-ob")
plt.show()

plt.plot(x_list_3[beaconNo-1], distance_list_3[beaconNo-1], "-ob")
plt.show()

plt.plot(x_list_5[beaconNo-1], distance_list_5[beaconNo-1], "-ob")
plt.show()