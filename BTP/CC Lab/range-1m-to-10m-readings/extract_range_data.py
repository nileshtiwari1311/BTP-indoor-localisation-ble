import json

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
				if reading["id3"] == 5 :
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