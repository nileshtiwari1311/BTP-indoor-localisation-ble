import json
import glob
import os

beacon_dict = {"beacon" : []}

data_dir = os.getcwd() + "/original-readings/"
# changes for each file of type myReading_x_y.json
for filename in glob.glob(os.path.join(data_dir, '*.json')):
	# with open(os.path.join(os.curdir(), filename), 'r') as f: 
	with open( filename, 'r') as f: 
		data = json.load(f)
		f.close()
		x_coord = data["x-coord"]
		y_coord = data["y-coord"]
		beacon_data_len = len(data["beaconReadings"])
		beacon_data = {}
		
		for i in range(0, beacon_data_len) :
			for reading in data["beaconReadings"][i]["readings"] :
				rssi = reading["rssi"]
				id3 = reading["id3"]
				address = reading["address"]
				distance = reading["distance"]
				if id3 in beacon_data :
					beacon_data[id3]["count"] += 1
					beacon_data[id3]["rssi"] += rssi
					beacon_data[id3]["distance"] += distance
				else :
					beacon_data[id3] = {"count" : 1, "rssi" : rssi, "id3" : id3, "distance" : distance, "address" : address}

		beacon_data_list = []
		for id3 in beacon_data :
			beacon_data_list.append({"id3" : id3, "address" : beacon_data[id3]["address"], "rssi" : beacon_data[id3]["rssi"]/beacon_data[id3]["count"], "distance" : beacon_data[id3]["distance"]/beacon_data[id3]["count"]})

		beacon_dict["beacon"].append({"x-coord" : x_coord, "y-coord" : y_coord, "beaconData" : beacon_data_list})

save_path = os.getcwd() + "/beacon-original/"
if not(os.path.isdir(save_path)) : 
	os.mkdir(save_path)
filename = "beacon.json"
filename = os.path.join(save_path, filename)
json_data = json.dumps(beacon_dict, indent = 4)
with open(filename, 'w') as f:
	f.write(json_data)