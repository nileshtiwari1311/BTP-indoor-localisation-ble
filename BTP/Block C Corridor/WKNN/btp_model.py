import json
import os
import glob

noOfBeacons = 6
noOfRefPoints = 18

for filterMethod in ["raw", "kalman", "movingAverage"] :
	for fd in range(3, noOfBeacons+1) :
		for k in range(3, noOfRefPoints+1) :
			mae_ble = 0
			mae_mag = 0
			sum_error_ble = 0
			sum_error_mag = 0

			max_error_ble = 0
			max_error_mag = 0

			min_error_ble = 100
			min_error_mag = 100

			rmse_x_ble = 0
			rmse_y_ble = 0
			rmse_x_mag = 0
			rmse_y_mag = 0
			sum_square_error_x_ble = 0
			sum_square_error_x_mag = 0
			sum_square_error_y_ble = 0
			sum_square_error_y_mag = 0

			count_error = 0
			scale_x = 0.6
			scale_y = 0.3

			mag_ref_points_data = {}
			ref_points_dir = os.getcwd() + "/geoMag-ref-points-" + filterMethod + "/"
			f = open(os.path.join(ref_points_dir, "geoMag.json"),"r")
			data = json.load(f)
			f.close()

			for it in data["geoMag"]:
				x_coord = it["x-coord"]
				y_coord = it["y-coord"]
				ref_point = (x_coord, y_coord)
				mag_ref_points_data[ref_point] = {"mx" : it['mx'], "my" : it['my'], "mz" : it['mz'], "MA" : it["MA"]}

			ble_ref_points_data = {}
			ref_points_dir = os.getcwd() + "/beacon-ref-points-" + filterMethod + "/"
			f = open(os.path.join(ref_points_dir, "beacon.json"),"r")
			data = json.load(f)
			f.close()

			for it in data["beacon"]:
				x_coord = it["x-coord"]
				y_coord = it["y-coord"]
				ref_point = (x_coord, y_coord)
				beacon_data = {}
				for reading in it["beaconData"]:
					beacon_data[reading["id3"]] = reading["rssi"]
				ble_ref_points_data[ref_point] = beacon_data

			mag_sample_points_data = {}
			sample_points_dir = os.getcwd() + "/geoMag-sample-points-" + filterMethod + "/"
			f = open(os.path.join(sample_points_dir, "geoMag.json"),"r")
			data = json.load(f)
			f.close()

			for it in data["geoMag"]:
				x_coord = it["x-coord"]
				y_coord = it["y-coord"]
				sample_point = (x_coord, y_coord)
				mag_sample_points_data[sample_point] = {"mx" : it['mx'], "my" : it['my'], "mz" : it['mz'], "MA" : it["MA"]}

			ble_sample_points_data = {}
			sample_points_dir = os.getcwd() + "/beacon-sample-points-" + filterMethod + "/"
			f = open(os.path.join(sample_points_dir, "beacon.json"),"r")
			data = json.load(f)
			f.close()

			for it in data["beacon"]:
				x_coord = it["x-coord"]
				y_coord = it["y-coord"]
				sample_point = (x_coord, y_coord)
				beacon_data = {}
				for reading in it["beaconData"]:
					beacon_data[reading["id3"]] = reading["rssi"]
				ble_sample_points_data[sample_point] = beacon_data

			mag_error_database = {}
			mag_error_coord_array = []

			print("Expected\t\tGeoMag\t\t\t\tAE")
			for sample_point in mag_sample_points_data :
				x_coord = sample_point[0]
				y_coord = sample_point[1]

				mx = mag_sample_points_data[sample_point]["mx"]
				my = mag_sample_points_data[sample_point]["my"]
				mz = mag_sample_points_data[sample_point]["mz"]
				MA = mag_sample_points_data[sample_point]["MA"]

				diffs = {}

				for ref_point in mag_ref_points_data:
					dx = mag_ref_points_data[ref_point]["mx"] - mx
					dy = mag_ref_points_data[ref_point]["my"] - my
					dz = mag_ref_points_data[ref_point]["mz"] - mz
					DA = mag_ref_points_data[ref_point]["MA"] - MA
					val = (dx*dx) + (dy*dy) + (dz*dz) + (DA*DA)
					val /= 4
					val = val**(0.5)
					diffs[ref_point] = val

				x_mag = 0
				y_mag = 0
				sumOfWeights = 0
				for ref_point in diffs:
					if diffs[ref_point] == 0:
						diffs[ref_point] = 0.001
					x_mag += (ref_point[0] / diffs[ref_point])
					y_mag += (ref_point[1] / diffs[ref_point])
					sumOfWeights += (1 / diffs[ref_point])

				x_mag /= sumOfWeights
				y_mag /= sumOfWeights

				errx = ((x_coord-x_mag)*scale_x)**2
				erry = ((y_coord-y_mag)*scale_y)**2
				err = (errx+erry)**(0.5)

				if err > max_error_mag :
					max_error_mag = err

				if err < min_error_mag :
					min_error_mag = err
				
				sum_error_mag += err
				sum_square_error_x_mag += errx
				sum_square_error_y_mag += erry
				
				print("x=" + str(x_coord) + "\t\tx=" + str(x_mag))
				print("y=" + str(y_coord) + "\t\ty=" + str(y_mag) + "\t\t" + str(err) + "\n")

				error_coord = {}
				error_coord["x-coord"] = x_coord
				error_coord["y-coord"] = y_coord
				error_coord["errx-mag"] = abs((x_coord-x_mag)*scale_x)
				error_coord["erry-mag"] = abs((y_coord-y_mag)*scale_y)
				error_coord["err-mag"] = err

				mag_error_coord_array.append(error_coord)

			ble_error_database = {}
			ble_error_coord_array = []

			print("Expected\t\tBLE\t\t\t\tAE")
			for sample_point in ble_sample_points_data :
				x_coord = sample_point[0]
				y_coord = sample_point[1]

				top_rssi = []
				for i in range(noOfBeacons) :
					beacon_dict = {}
					beacon_dict["rssi"] = ble_sample_points_data[sample_point][i+1]
					beacon_dict["id3"] = i+1
					top_rssi.append(beacon_dict)

				top_rssi = sorted(top_rssi, key = lambda i: i['rssi'], reverse=True)
				top_rssi = top_rssi[:fd]

				diffs = {}
				for ref_point in ble_ref_points_data :
					val = 0
					for item in top_rssi :
						id3 = item["id3"]
						val += (ble_sample_points_data[sample_point][id3] - ble_ref_points_data[ref_point][id3])**2
					val = val**(0.5)
					diffs[ref_point] = val

				diffs = sorted(diffs.items(), key=lambda item: item[1])
				diffs = diffs[:k]
				diffs = dict(diffs)

				x_ble = 0
				y_ble = 0
				sumOfWeights = 0
				for ref_point in diffs:
					if diffs[ref_point] == 0:
						diffs[ref_point] = 0.001
					x_ble += (ref_point[0] / diffs[ref_point])
					y_ble += (ref_point[1] / diffs[ref_point])
					sumOfWeights += (1 / diffs[ref_point])

				x_ble /= sumOfWeights
				y_ble /= sumOfWeights

				errx = ((x_coord-x_ble)*scale_x)**2
				erry = ((y_coord-y_ble)*scale_y)**2
				err = (errx+erry)**(0.5)

				if err > max_error_ble :
					max_error_ble = err

				if err < min_error_ble :
					min_error_ble = err
				
				sum_error_ble += err
				sum_square_error_x_ble += errx
				sum_square_error_y_ble += erry

				print("x=" + str(x_coord) + "\t\tx=" + str(x_ble))
				print("y=" + str(y_coord) + "\t\ty=" + str(y_ble) + "\t\t" + str(err) + "\n")

				error_coord = {}
				error_coord["x-coord"] = x_coord
				error_coord["y-coord"] = y_coord
				error_coord["errx-ble"] = abs((x_coord-x_ble)*scale_x)
				error_coord["erry-ble"] = abs((y_coord-y_ble)*scale_y)
				error_coord["err-ble"] = err

				ble_error_coord_array.append(error_coord)
				count_error += 1

			mag_error_database["error-coord"] = mag_error_coord_array
			ble_error_database["error-coord"] = ble_error_coord_array

			mae_ble = sum_error_ble/count_error
			mae_mag = sum_error_mag/count_error
			rmse_x_ble = (sum_square_error_x_ble/count_error)**0.5
			rmse_y_ble = (sum_square_error_y_ble/count_error)**0.5
			rmse_x_mag = (sum_square_error_x_mag/count_error)**0.5
			rmse_y_mag = (sum_square_error_y_mag/count_error)**0.5

			ble_error_database["mae-ble"] = mae_ble
			mag_error_database["mae-mag"] = mae_mag
			ble_error_database["rmse-ble-x"] = rmse_x_ble
			ble_error_database["rmse-ble-y"] = rmse_y_ble
			mag_error_database["rmse-mag-x"] = rmse_x_mag
			mag_error_database["rmse-mag-y"] = rmse_y_mag
			ble_error_database["max-error-ble"] = max_error_ble
			mag_error_database["max-error-mag"] = max_error_mag
			ble_error_database["min-error-ble"] = min_error_ble
			mag_error_database["min-error-mag"] = min_error_mag

			ble_error_database["k"] = k
			ble_error_database["fd"] = fd
			ble_error_database["filter"] = filterMethod

			print("mae_ble = " + str(mae_ble))
			print("max_error_ble = " + str(max_error_ble))
			print("rmse_x_ble = " + str(rmse_x_ble))
			print("rmse_y_ble = " + str(rmse_y_ble))

			save_path = os.getcwd() + "/error-database/"
			if not(os.path.isdir(save_path)) : 
				os.mkdir(save_path)

			# errorfile = "geoMag_error_database.json"
			# errorfile = os.path.join(save_path, errorfile)
			# json_data = json.dumps(mag_error_database, indent = 4)
			# with open(errorfile, 'w') as f:
			# 	f.write(json_data)

			errorfile = "beacon_error_database_" + filterMethod + "_k" + str(k) + "_fd" + str(fd) + ".json"
			errorfile = os.path.join(save_path, errorfile)
			json_data = json.dumps(ble_error_database, indent = 4)
			with open(errorfile, 'w') as f:
				f.write(json_data)