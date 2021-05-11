import json
import glob
import os
from filters import kalman
from filters import raw
from filters import movingAverage

def get_filter_ble(name, noOfBeacons, kalmanRBLE, kalmanQBLE, windowSizeBLE) :
	if name == "raw" :
		return [raw.RawFilter() for i in range(noOfBeacons)]
	if name == "kalman" :
		return [kalman.KalmanFilter(kalmanRBLE, kalmanQBLE) for i in range(noOfBeacons)]
	if name == "movingAverage" :
		return [movingAverage.MovingAverageFilter(windowSizeBLE) for i in range(noOfBeacons)]

def get_filter_mag(name, kalmanRMag, kalmanQMag, windowSizeMag) :
	if name == "raw" :
		return raw.RawFilter()
	if name == "kalman" :
		return kalman.KalmanFilter(kalmanRMag, kalmanQMag)
	if name == "movingAverage" :
		return movingAverage.MovingAverageFilter(windowSizeMag)

def generate_json(data_dir, filterNameBLE, filterNameMag, kalmanRBLE, kalmanRMag, kalmanQBLE, kalmanQMag, windowSizeBLE, windowSizeMag, noOfBeacons) :
	geoMag_dict = {"geoMag" : []}
	beacon_dict = {"beacon" : []}

	for filename in glob.glob(os.path.join(data_dir, '*.json')):
		with open( filename, 'r') as f: 
			data = json.load(f)
			f.close()
			x_coord = data["x-coord"]
			y_coord = data["y-coord"]

			mag_data_len = len(data["geoMagReadings"])
			filterMag = get_filter_mag(filterNameMag, kalmanRMag, kalmanQMag, windowSizeMag)
			mx = 0
			my = 0
			mz = 0
			MA = 0
			for i in range(0, mag_data_len):
				mx += filterMag.filter(data["geoMagReadings"][i]["mx"])
				my += filterMag.filter(data["geoMagReadings"][i]["my"])
				mz += filterMag.filter(data["geoMagReadings"][i]["mz"])
				MA += filterMag.filter(data["geoMagReadings"][i]["MA"])

			mx /= mag_data_len
			my /= mag_data_len
			mz /= mag_data_len
			MA /= mag_data_len

			geoMag_dict["geoMag"].append({"x-coord" : x_coord, "y-coord" : y_coord, "mx" : mx, "my" : my, "mz" : mz, "MA" : MA})

			beacon_data_len = len(data["beaconReadings"])
			filterBLE = get_filter_ble(filterNameBLE, noOfBeacons, kalmanRBLE, kalmanQBLE, windowSizeBLE)
			beacon_data = {}
			for i in range(0, beacon_data_len) :
				for reading in data["beaconReadings"][i]["readings"] :
					rssi = reading["rssi"]
					id3 = reading["id3"]
					address = reading["address"]
					distance = reading["distance"]
					if id3 in beacon_data :
						beacon_data[id3]["count"] += 1
						beacon_data[id3]["rssi"] += filterBLE[id3-1].filter(rssi)
						beacon_data[id3]["distance"] += distance
					else :
						beacon_data[id3] = {"count" : 1, "rssi" : filterBLE[id3-1].filter(rssi), "id3" : id3, "distance" : distance, "address" : address}

			beacon_data_list = []
			for id3 in beacon_data :
				beacon_data_list.append({"id3" : id3, "address" : beacon_data[id3]["address"], "rssi" : beacon_data[id3]["rssi"]/beacon_data[id3]["count"], "distance" : beacon_data[id3]["distance"]/beacon_data[id3]["count"]})

			beacon_dict["beacon"].append({"x-coord" : x_coord, "y-coord" : y_coord, "beaconData" : beacon_data_list})

	save_path = os.getcwd() + "/geoMag-ref-points-" + filterMag.get_name() + "/"
	if not(os.path.isdir(save_path)) : 
		os.mkdir(save_path)
	filename = "geoMag.json"
	filename = os.path.join(save_path, filename)
	json_data = json.dumps(geoMag_dict, indent = 4)
	with open(filename, 'w') as f:
		f.write(json_data)

	save_path = os.getcwd() + "/beacon-ref-points-" + filterBLE[0].get_name() + "/"
	if not(os.path.isdir(save_path)) : 
		os.mkdir(save_path)
	filename = "beacon.json"
	filename = os.path.join(save_path, filename)
	json_data = json.dumps(beacon_dict, indent = 4)
	with open(filename, 'w') as f:
		f.write(json_data)

data_dir = os.getcwd() + "/ref-points-readings/"
noOfBeacons = 10
filterNameBLE = "kalman"
filterNameMag = "kalman"
kalmanRBLE = 0.008
kalmanRMag = 0.008
kalmanQBLE = 1.0
kalmanQMag = 1.0
windowSizeBLE = 5
windowSizeMag = 5
generate_json(data_dir, filterNameBLE, filterNameMag, kalmanRBLE, kalmanRMag, kalmanQBLE, kalmanQMag, windowSizeBLE, windowSizeMag, noOfBeacons)