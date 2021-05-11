from matplotlib import pyplot as plt 
import json
import os
import operator

filterMethod = "kalman"

data_dir = os.getcwd() + "/beacon-all-points-" + filterMethod + "/"
f = open(os.path.join(data_dir, "beacon.json"),"r")
data = json.load(f)
f.close()

save_path = os.getcwd() + "/Graphs/rssi_vs_distance_reported/"
if not(os.path.isdir(save_path)) : 
	os.mkdir(save_path)

distance = {}
rssi = {}
noOfBeacons = 10

for elem in data["beacon"]:
	for values in elem["beaconData"]:
		if values["id3"] in distance :
			distance[values["id3"]].append(values["distance"])
		else :
			distance[values["id3"]] = [values["distance"]]

		if values["id3"] in rssi :
			rssi[values["id3"]].append(values["rssi"])
		else :
			rssi[values["id3"]] = [values["rssi"]]
		
for beaconNo in range(1, noOfBeacons+1) :
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
	filename = os.path.join(save_path, "rssi_vs_distance_" + str(beaconNo))
	plt.savefig(filename, dpi=200, bbox_inches='tight')
	plt.close()