from matplotlib import pyplot as plt 
import json
import os
from filters import kalman

kalmanR = 0.008
kalmanQ = 1.0

final_readings_dir = os.getcwd() + "/final-readings/"
f = open(os.path.join(final_readings_dir, "myReading_7_18.json"),"r")
data = json.load(f)
f.close()

save_path = os.getcwd() + "/Graphs/rssi_vs_sampling_times/"
if not(os.path.isdir(save_path)) : 
	os.mkdir(save_path)

rssi_dict = {}
noOfBeacons = 10

for sample in data["beaconReadings"] :
	for reading in sample["readings"] :
		if reading["id3"] in rssi_dict:
			rssi_dict[reading["id3"]].append(reading["rssi"])
		else :
			rssi_dict[reading["id3"]] = [reading["rssi"]]

for beaconNo in range(1, noOfBeacons+1) :
	plt.figure(figsize=(16, 10))
	plt.title("RSSI vs Sampling times")
	plt.xlabel("Sampling times") 
	plt.ylabel("RSSI in dBm")
	kalmanFilter = kalman.KalmanFilter(kalmanR, kalmanQ)
	filteredRSSI = []
	for rssi in rssi_dict[beaconNo] :
		filteredRSSI.append(kalmanFilter.filter(rssi))
	plt.plot([x for x in range(1, len(rssi_dict[beaconNo])+1)], rssi_dict[beaconNo], "-ob")
	plt.plot([x for x in range(1, len(rssi_dict[beaconNo])+1)], filteredRSSI, "-og")
	plt.legend(["Raw","Kalman Filter"])
	# plt.show()
	filename = os.path.join(save_path, "rssi_vs_sampling_times_" + str(beaconNo))
	plt.savefig(filename, dpi=200, bbox_inches='tight')
	plt.close()