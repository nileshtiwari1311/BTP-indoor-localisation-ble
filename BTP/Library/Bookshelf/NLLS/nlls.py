import json
import os
import numpy as np

noOfBeacons = 10

for filterMethod in ["raw", "kalman", "movingAverage"] :
	for fd in range(3, noOfBeacons+1) :
		mae_ble = 0
		sum_error_ble = 0
		max_error_ble = 0
		min_error_ble = 100

		rmse_x_ble = 0
		rmse_y_ble = 0
		sum_square_error_x_ble = 0
		sum_square_error_y_ble = 0

		count_error = 0

		scaleX = 0.3
		scaleY = 0.3
		stepX = 0.5
		stepY = 0.5

		max_x = 28 + stepX #(of space to do exhaustive search)
		max_y = 58 + stepY

		x_range = np.arange(0.0, max_x, stepX).tolist()
		y_range = np.arange(44.0, max_y, stepY).tolist()

		noOfBeacons = 10

		parameter_dir = os.getcwd() + "/Path-Loss-Model/"
		f = open(os.path.join(parameter_dir, "path_loss_parameters.json"), "r")
		data = json.load(f)
		f.close()

		ai = [0 for i in range(noOfBeacons)]
		bi = [0 for i in range(noOfBeacons)]

		for it in data["model"]["parameters"] :
			id3 = it["id3"]
			ai[id3-1] = it["a"]
			bi[id3-1] = it["b"]

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

		#  beacons ka position
		xi = [20,10,28,0,28,12,0,22,14,4]
		yi = [0,0,20,20,40,42,40,58,58,58]

		x = sum(xi)/len(xi) # initialise x,y coordinates with average x and y
		y = sum(yi)/len(yi)
		xfinal = x
		yfinal = y

		ble_error_database = {}
		ble_error_coord_array = []

		print("Expected\t\tBLE\t\t\t\tAE")
		for sample_point in ble_sample_points_data :
			x_coord = sample_point[0]
			y_coord = sample_point[1]
			mindiff = 100000000

			top_rssi = []
			for i in range(noOfBeacons) :
				beacon_dict = {}
				beacon_dict["rssi"] = ble_sample_points_data[sample_point][i+1]
				beacon_dict["id3"] = i+1
				top_rssi.append(beacon_dict)

			top_rssi = sorted(top_rssi, key = lambda i: i['rssi'], reverse=True)
			top_rssi = top_rssi[:fd]

			di = [-1.0 for i in range(noOfBeacons)]
			for item in top_rssi :
				id3 = item["id3"]
				estimated_d = 10**((item["rssi"] - ai[id3-1]) / bi[id3-1])
				di[id3-1] = estimated_d

			# as the sample space is small we can check for all possible (x,y) with step size of 0.15m along both axes in test bed 
			for aa in x_range:
				for bb in y_range:
					x = aa
					y = bb
					tsum = 0
					for i in range(0, noOfBeacons):
						if di[i] != -1.0 :
							xdiff = ( (xi[i] - x)*scaleX )**2
							ydiff = ( (yi[i] - y)*scaleY )**2
							tdiff = ( xdiff + ydiff )**0.5
							tsum += (  tdiff - di[i] )**2

					if(tsum < mindiff):
						mindiff = tsum
						xfinal = x
						yfinal = y

			x_ble = xfinal
			y_ble = yfinal

			errx = ((x_coord-x_ble)*scaleX)**2
			erry = ((y_coord-y_ble)*scaleY)**2
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
			error_coord["errx-ble"] = abs((x_coord-x_ble)*scaleX)
			error_coord["erry-ble"] = abs((y_coord-y_ble)*scaleY)
			error_coord["err-ble"] = err

			ble_error_coord_array.append(error_coord)
			count_error += 1

		ble_error_database["error-coord"] = ble_error_coord_array

		mae_ble = sum_error_ble/count_error
		rmse_x_ble = (sum_square_error_x_ble/count_error)**0.5
		rmse_y_ble = (sum_square_error_y_ble/count_error)**0.5

		ble_error_database["mae-ble"] = mae_ble
		ble_error_database["rmse-ble-x"] = rmse_x_ble
		ble_error_database["rmse-ble-x"] = rmse_x_ble
		ble_error_database["rmse-ble-y"] = rmse_y_ble
		ble_error_database["max-error-ble"] = max_error_ble
		ble_error_database["min-error-ble"] = min_error_ble

		ble_error_database["fd"] = fd
		ble_error_database["filter"] = filterMethod

		print("mae_ble = " + str(mae_ble))
		print("max_error_ble = " + str(max_error_ble))
		print("rmse_x_ble = " + str(rmse_x_ble))
		print("rmse_y_ble = " + str(rmse_y_ble))

		save_path = os.getcwd() + "/error-database/"
		if not(os.path.isdir(save_path)) : 
			os.mkdir(save_path)

		errorfile = "beacon_error_database_" + filterMethod + "_fd" + str(fd) + ".json"
		errorfile = os.path.join(save_path, errorfile)
		json_data = json.dumps(ble_error_database, indent = 4)
		with open(errorfile, 'w') as f:
			f.write(json_data)