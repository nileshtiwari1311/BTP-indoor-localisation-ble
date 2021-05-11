from matplotlib import pyplot as plt 
import matplotlib as mpl
import numpy as np
import json
import os

beaconNo = 3

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
plt.title("RSSI vs Time", fontsize=20)
plt.xlabel("Time in seconds", fontsize=20) 
plt.ylabel("RSSI in dBm", fontsize=20)
plt.yticks(np.arange(-85, -59, 5.0), fontsize=15)
plt.xticks(np.arange(0, 301, 50), fontsize=15)
plt.xlim([0, 301])
plt.ylim([-85, -59])
plt.grid()
plt.plot([x for x in range(1, 301)], rssi_list, "-b")
filename = os.path.join(save_path, "rssi_vs_time_beacon" + str(beaconNo))
plt.savefig(filename)
plt.close()