import json
import os
import glob
import random

save_path = os.getcwd() + "/corrected-json/"
if not(os.path.isdir(save_path)) : 
	os.mkdir(save_path)

rssi_list = []
distance_list = []
for i in range(0,19) :
	rssi_list.append(-1.0*random.randrange(8958000, 9555556)/100000)
	distance_list.append(random.randrange(202488, 302764)/100000)

rssi_list.sort()
distance_list.sort()

counter = 0
json_dir = os.getcwd() + "/missing-values/"
for filename in glob.glob(os.path.join(json_dir, '*.json')):
	with open(filename, 'r') as f: 
		data = json.load(f)
		f.close()
		x_coord = data["x-coord"]
		y_coord = data["y-coord"]

		for reading in data["beaconReadings"] :
			if reading["numOfBeacons"] < 6 :
				reading["numOfBeacons"] += 1
				beacon_dict = {"id1": "0c5e264e-b1c1-4d6d-9ce9-86e0e380af00", "id2": 100, "id3": 1, "address": "0C:F3:EE:B5:B3:B9"}
				beacon_dict["rssi"] = rssi_list[counter]
				beacon_dict["distance"] = distance_list[counter]
				reading["readings"].append(beacon_dict)
				
		counter+=1

		newfile = "myReading_" + str(x_coord) + "_" + str(y_coord) + ".json"
		newfile = os.path.join(save_path, newfile)
		json_data = json.dumps(data, indent = 4)
		with open(newfile, 'w') as f:
			f.write(json_data)