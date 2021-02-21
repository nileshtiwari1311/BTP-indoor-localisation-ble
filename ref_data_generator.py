import json
import glob
import os

geo_mag_arr_ref = {"geoMagRef" : []} #iska size ref_point_size hoga
beacon_arr_ref = {"beaconRef" : []}

ref_dir = os.getcwd() + "/BTP-readings/"
# changes for each file of type myReading_x_y.json
for filename in glob.glob(os.path.join(ref_dir, '*.json')):
	# with open(os.path.join(os.curdir(), filename), 'r') as f: 
	with open( filename, 'r') as f: 
		data = json.load(f)
		f.close()
		x_coord = data["x-coord"]
		y_coord = data["y-coord"]
		mag_data_len = len(data["geoMagReadings"])
		beacon_data_len = len(data["beaconReadings"])
		beacon_data = {}
		mx = 0
		my = 0
		mz = 0
		MA = 0
		for i in range(0,mag_data_len):
			mx+=data["geoMagReadings"][i]["mx"]
			my+=data["geoMagReadings"][i]["my"]
			mz+=data["geoMagReadings"][i]["mz"]
			MA+=data["geoMagReadings"][i]["MA"]

		mx/=mag_data_len
		my/=mag_data_len
		mz/=mag_data_len
		MA/=mag_data_len

		geo_mag_arr_ref["geoMagRef"].append({"x-coord" : x_coord, "y-coord" : y_coord, "mx" : mx, "my" : my, "mz" : mz, "MA" : MA})

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

save_path = os.getcwd() + "/geoMagRef/"
if not(os.path.isdir(save_path)) : 
	os.mkdir(save_path)
filename = "geoMagRef.json"
filename = os.path.join(save_path, filename)
json_data = json.dumps(geo_mag_arr_ref, indent = 4)
with open(filename, 'w') as f:
	f.write(json_data)

save_path = os.getcwd() + "/beaconRef/"
if not(os.path.isdir(save_path)) : 
	os.mkdir(save_path)
filename = "beaconRef.json"
filename = os.path.join(save_path, filename)
json_data = json.dumps(beacon_arr_ref, indent = 4)
with open(filename, 'w') as f:
	f.write(json_data)