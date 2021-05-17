import os
import json
import glob

error_data = {}
error_list = []

for filename in glob.glob('*.json'):
	with open (filename, 'r') as f:
		data = json.load(f)
		f.close()

		single_dict = {}
		single_dict["mae-ble"] = data["mae-ble"]
		single_dict["rmse-ble-x"] = data["rmse-ble-x"]
		single_dict["rmse-ble-y"] = data["rmse-ble-y"]
		single_dict["max-error-ble"] = data["max-error-ble"]
		single_dict["min-error-ble"] = data["min-error-ble"]
		single_dict["fd"] = data["fd"]
		single_dict["filter"] = data["filter"]

		error_list.append(single_dict)

error_data["values"] = error_list

newfile = "beacon_error_database_complete.json"
json_data = json.dumps(error_data, indent=4)
with open(newfile, 'w') as f:
	f.write(json_data)
