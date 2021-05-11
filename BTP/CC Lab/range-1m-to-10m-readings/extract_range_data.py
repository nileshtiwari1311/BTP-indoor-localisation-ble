import json
from matplotlib import pyplot as plt
import numpy as np
import os

beaconNos = [5, 7]

for beaconNo in beaconNos :
	range_data = {}
	range_data["beaconNo"] = beaconNo
	readings_list = []

	for i in range(1, 11) :
		f = open('myReading_beacon' + str(beaconNo) + '_' + str(i) + 'm.json', 'r')
		data = json.load(f)
		f.close()

		distance = i
		fixed_distance_data = {}
		fixed_distance_data["distance"] = distance
		data_list = []

		for item in data["beaconReadings"] :
			for reading in item["readings"] :
				if reading["id3"] == beaconNo :
					reading_dict = {}
					reading_dict["rssi"] = reading["rssi"]
					reading_dict["distance"] = reading["distance"]
					data_list.append(reading_dict)

		fixed_distance_data["samples"] = data_list
		readings_list.append(fixed_distance_data)

	range_data["readings"] = readings_list

	newfile = "myReading_beacon" + str(beaconNo) + ".json"
	json_data = json.dumps(range_data, indent = 4)
	with open(newfile, 'w') as f:
		f.write(json_data)

	rssi_distance_map = {}
	rssi_distance_list = []
	for item in range_data["readings"] :
		reading_dict = {}
		distance = item["distance"]
		reading_dict["distance"] = distance
		rssi = 0
		count = 0
		for sample in item["samples"] :
			rssi += sample["rssi"]
			count += 1

		rssi = rssi/count
		reading_dict["rssi"] = rssi
		rssi_distance_list.append(reading_dict)

	rssi_distance_map["readings"] = rssi_distance_list

	newfile = "myReading_range_1m_to_10m_beacon" + str(beaconNo) + ".json"
	json_data = json.dumps(rssi_distance_map, indent = 4)
	with open(newfile, 'w') as f:
		f.write(json_data)

	rssi_list = [x["rssi"] for x in rssi_distance_list]
	distance_list = [x["distance"] for x in rssi_distance_list]
	save_path = os.getcwd() + "/Graphs/rssi_vs_distance/"
	if not(os.path.isdir(save_path)) : 
		os.mkdir(save_path)

	plt.figure(figsize=(16, 10))
	plt.title("RSSI vs Distance", fontsize=15)
	plt.xlabel("Distance in m", fontsize=15) 
	plt.ylabel("RSSI in dBm", fontsize=15)
	plt.yticks(np.arange(-100, -39, 5.0), fontsize=12)
	plt.xticks(np.arange(0, 11, 1.0), fontsize=12)
	plt.xlim([0, 11])
	plt.ylim([-100, -39])
	plt.grid()
	plt.plot(distance_list, rssi_list, "-ob")
	filename = os.path.join(save_path, "rssi_vs_distance_beacon" + str(beaconNo))
	plt.savefig(filename)
	plt.close()