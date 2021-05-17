from matplotlib import pyplot as plt 
import matplotlib as mpl
import numpy as np
import json
import os
from filters import kalman
from filters import raw
from filters import movingAverage

beaconNo = 3

kalmanR = 0.008
kalmanQ = 1.0

sample_data = {}
sample_data["beaconNo"] = beaconNo
sample_data["id3"] = beaconNo
sample_data["address"] = "0C:F3:EE:B5:BB:10"
data_list = []

for i in range(1, 7) :
	f = open("myReading_0_" + str(i) + ".json")
	data = json.load(f)
	f.close()

	for item in data["beaconReadings"] :
		for reading in item["readings"] :
			if reading["id3"] == beaconNo :
				reading_dict = {}
				reading_dict["rssi"] = reading["rssi"]
				reading_dict["distance"] = reading["distance"]
				data_list.append(reading_dict)

sample_data["readings"] = data_list
newfile = "myReading_5min_beacon" + str(beaconNo) + ".json"
json_data = json.dumps(sample_data, indent = 4)
with open(newfile, 'w') as f:
	f.write(json_data)

rssi_list = [x["rssi"] for x in data_list]
save_path = os.getcwd() + "/Graphs/rssi_vs_time/"
if not(os.path.isdir(save_path)) : 
	os.mkdir(save_path)

plt.figure(figsize=(16, 10))
plt.xlabel("Time in seconds", fontsize=20) 
plt.ylabel("RSSI in dBm", fontsize=20)
plt.yticks(np.arange(-85, -59, 5.0), fontsize=20)
plt.xticks(np.arange(0, 301, 50), fontsize=20)
plt.xlim([0, 301])
plt.ylim([-85, -59])
plt.grid()
kalmanFilter = kalman.KalmanFilter(kalmanR, kalmanQ)
kalman_list = []
for rssi in rssi_list :
	kalman_list.append(kalmanFilter.filter(rssi))
movingAverageFilter = movingAverage.MovingAverageFilter(5)
moving_list = []
for rssi in rssi_list :
	moving_list.append(movingAverageFilter.filter(rssi))
plt.plot([x for x in range(1, 301)], rssi_list, "-b")
plt.plot([x for x in range(1, 301)], kalman_list, "-r")
plt.plot([x for x in range(1, 301)], moving_list, "-g")
plt.legend(["Raw","Kalman Filter", "Moving Average"], fontsize=20)
filename = os.path.join(save_path, "rssi_vs_time_beacon" + str(beaconNo))
plt.savefig(filename)
plt.close()