from matplotlib import pyplot as plt 
import json
import os
import operator

ref_dir = os.getcwd() + "/beaconRef/"
f = open(os.path.join(ref_dir, "beaconRef.json"),"r")
data = json.load(f)
f.close()

save_dir = os.getcwd() + "/Graphs/rssi_vs_distance_reported/"
if not(os.path.isdir(save_dir)) : 
	os.mkdir(save_dir)

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
		
for beaconNo in range(1,7) :
	plt.figure(figsize=(16, 10))
	plt.title("Variation in RSSI vs reported distance from beacon " + str(beaconNo)) 
	plt.xlabel("Distance in meters") 
	plt.ylabel("RSSI in dBm") 
	sort_axis = operator.itemgetter(0)
	sorted_zip = sorted(zip(distance[beaconNo], rssi[beaconNo]), key=sort_axis)
	sort_distance, sort_rssi = zip(*sorted_zip)
	plt.plot(sort_distance, sort_rssi, "-ob")  
	plt.grid()
	# plt.show()
	filename = os.path.join(save_dir, "rssi_vs_distance_" + str(beaconNo))
	plt.savefig(filename, dpi=200, bbox_inches='tight')
	plt.close()