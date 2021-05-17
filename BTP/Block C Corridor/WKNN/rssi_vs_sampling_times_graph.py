from matplotlib import pyplot as plt 
import json
import os
from filters import kalman
from filters import movingAverage

kalmanR = 0.008
kalmanQ = 1.0

final_readings_dir = os.getcwd() + "/final-readings/"
f = open(os.path.join(final_readings_dir, "myReading_9_3.json"),"r")
data = json.load(f)
f.close()

save_path = os.getcwd() + "/Graphs/rssi_vs_sampling_times/"
if not(os.path.isdir(save_path)) : 
	os.mkdir(save_path)

rssi_dict = {}
noOfBeacons = 6

for sample in data["beaconReadings"] :
	for reading in sample["readings"] :
		if reading["id3"] in rssi_dict:
			rssi_dict[reading["id3"]].append(reading["rssi"])
		else :
			rssi_dict[reading["id3"]] = [reading["rssi"]]

for beaconNo in range(1, noOfBeacons+1) :
	plt.figure(figsize=(16, 10))
	# plt.title("RSSI vs Sampling times")
	plt.xlabel("Sampling times",fontsize=20) 
	plt.ylabel("RSSI in dBm",fontsize=20)
	plt.xticks(fontsize=20)
	plt.yticks(fontsize=20)
	plt.xlim([0, len(rssi_dict[beaconNo])+1])
	plt.ylim([-100, -49])
	kalmanFilter = kalman.KalmanFilter(kalmanR, kalmanQ)
	kalmanRSSI = []
	for rssi in rssi_dict[beaconNo] :
		kalmanRSSI.append(kalmanFilter.filter(rssi))
	movingAverageFilter = movingAverage.MovingAverageFilter(5)
	moving_list = []
	for rssi in rssi_dict[beaconNo] :
		moving_list.append(movingAverageFilter.filter(rssi))
	plt.grid()
	plt.plot([x for x in range(1, len(rssi_dict[beaconNo])+1)], rssi_dict[beaconNo], "-ob")
	plt.plot([x for x in range(1, len(rssi_dict[beaconNo])+1)], kalmanRSSI, "-or")
	plt.plot([x for x in range(1, len(rssi_dict[beaconNo])+1)], moving_list, "-og")
	plt.legend(["Raw","Kalman","Moving Average"], fontsize=20)
	# plt.show()
	filename = os.path.join(save_path, "rssi_vs_sampling_times_" + str(beaconNo))
	plt.savefig(filename, dpi=200, bbox_inches='tight')
	plt.close()