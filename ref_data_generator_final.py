import json
import glob
import os

beacon_arr_ref = {"beaconRef" : []}

ref_dir = os.getcwd() + "/BTP-readings-model/"
# changes for each file of type myReading_x_y.json
for filename in glob.glob(os.path.join(ref_dir, '*.json')):
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
				if address in beacon_data :
					beacon_data[address]["count"]+=1
					beacon_data[address]["rssi"]+=rssi
					beacon_data[address]["distance"]+=distance
				else :
					beacon_data[address] = {"count" : 1, "rssi" : rssi, "id3" : id3, "distance" : distance}

		beacon_data_list = []
		for addr in beacon_data :
			beacon_data_list.append({"id3" : beacon_data[addr]["id3"], "address" : addr, "rssi" : beacon_data[addr]["rssi"]/beacon_data[addr]["count"], "distance" : beacon_data[addr]["distance"]/beacon_data[addr]["count"]})

		beacon_arr_ref["beaconRef"].append({"x-coord" : x_coord, "y-coord" : y_coord, "beaconData" : beacon_data_list})

save_path = os.getcwd() + "/beaconRef/"
if not(os.path.isdir(save_path)) : 
	os.mkdir(save_path)
filename = "beaconRef.json"
filename = os.path.join(save_path, filename)
json_data = json.dumps(beacon_arr_ref, indent = 4)
with open(filename, 'w') as f:
	f.write(json_data)