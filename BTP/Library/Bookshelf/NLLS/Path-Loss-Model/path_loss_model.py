import json
import os
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

f = open("rssi_distance.json")
data = json.load(f)
f.close()

noOfBeacons = 10
a_beacon = []
for i in range(1, noOfBeacons+1) :
	for item in data[str(i)] :
		if item["distance"] == 1.0 :
			a_beacon.append(item["rssi"])

parameter_dict = {}
parameter_list_scipy_a = []

for id3 in range(1, noOfBeacons+1) :
	rssi_list = []
	distance_list = []
	data[str(id3)] = sorted(data[str(id3)], key = lambda i: i['distance'])
	rssi_list = [x["rssi"] for x in data[str(id3)]]
	distance_list = [x["distance"] for x in data[str(id3)]]

	x = np.array(distance_list)
	y = np.array(rssi_list)

	# scipy optimize to fit rssi against log10(distance) with fixed A(rssi at 1m)
	z_scipy_a = curve_fit(lambda t,b: b*np.log10(t)+a_beacon[id3-1], x, y)
	z_scipy_a = z_scipy_a[0].tolist()
	z_scipy_a.reverse()
	print(z_scipy_a)

	id3_dict_scipy_a = {}
	id3_dict_scipy_a["id3"] = id3
	id3_dict_scipy_a["b"] = round(z_scipy_a[0], 2)
	id3_dict_scipy_a["a"] = a_beacon[id3-1]
	parameter_list_scipy_a.append(id3_dict_scipy_a)

	# Graph
	# plt.plot(distance_list, rssi_list, "xb")
	# plt.plot(distance_list, [z_scipy_a[0]*np.log10(it) + a_beacon[id3-1] for it in distance_list], "-r")
	# plt.show()

parameter_dict["model"] = {"d0": 1.0, "parameters": parameter_list_scipy_a}

newfile = "path_loss_parameters.json"
json_data = json.dumps(parameter_dict, indent=4)
with open(newfile, 'w') as f:
	f.write(json_data)
