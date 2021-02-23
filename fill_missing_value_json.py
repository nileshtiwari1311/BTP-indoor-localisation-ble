import json
import os
import glob

save_path = os.getcwd() + "/corrected-values-json/"
if not(os.path.isdir(save_path)) : 
	os.mkdir(save_path)

rssi_list_1 = [-93.76550939984494, -93.73444212842611, -93.48592415265531, -93.0661869976001, -92.52817943777592, -91.93156749714603]
distance_list_1 = [2.7126305519655887, 2.7073516429282165, 2.665635973741587, 2.5972018050092345, 2.5130567957854737, 2.4242028673807]

rssi_list_3 = [-96.02373560824489, -96.24537458861957, -96.18926588475158, -95.89496403746683, -95.41012253687545, -94.79049382237181]
distance_list_3 = [3.0562237200020306, 3.09827696950736, 3.0875666555633003, 3.032101315657421, 2.9432796023988246, 2.8342228838803223]

rssi_list_5 = [-92.84848910911505, -93.12445400911051, -93.26254063114618, -93.29841186161869, -93.26753461767265, -93.20517984720072, -93.14642252884377]
distance_list_5 = [2.5241024106471173, 2.564767705873294, 2.5854990225104757, 2.590927033127514, 2.586253651571951, 2.576855819897446, 2.5680485992622266]

list_1_counter = 0
list_3_counter = 0
list_5_counter = 0

json_dir = os.getcwd() + "/missing-values-json/"
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
				if y_coord == 1 :
					beacon_dict["rssi"] = rssi_list_1[list_1_counter]
					beacon_dict["distance"] = distance_list_1[list_1_counter]
					reading["readings"].append(beacon_dict)
				elif y_coord == 3 :
					beacon_dict["rssi"] = rssi_list_3[list_3_counter]
					beacon_dict["distance"] = distance_list_3[list_3_counter]
					reading["readings"].append(beacon_dict)
				else :
					beacon_dict["rssi"] = rssi_list_5[list_5_counter]
					beacon_dict["distance"] = distance_list_5[list_5_counter]
					reading["readings"].append(beacon_dict)
		
		if y_coord == 1 :	
			list_1_counter+=1
		elif y_coord == 3 :
			list_3_counter+=1
		else :
			list_5_counter+=1

		newfile = "myReading_" + str(x_coord) + "_" + str(y_coord) + ".json"
		newfile = os.path.join(save_path, newfile)
		json_data = json.dumps(data, indent = 4)
		with open(newfile, 'w') as f:
			f.write(json_data)