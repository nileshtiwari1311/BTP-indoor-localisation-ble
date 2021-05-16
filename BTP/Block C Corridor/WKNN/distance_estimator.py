from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
import numpy as np 
from matplotlib import pyplot as plt 
import json
import os

def fit_missing_distance(rssi_list, distance_list, poly_degree, x_pred_list) :
	x = np.array(rssi_list)
	X = x.reshape(-1, 1)
	y = np.array(distance_list)
	Y = y.reshape(-1, 1)

	polynomial_features = PolynomialFeatures(degree=poly_degree)
	x_poly = polynomial_features.fit_transform(X)

	model = LinearRegression()
	model.fit(x_poly, Y)

	x_pred = np.array(x_pred_list).reshape(-1,1)
	x_pred_transform = polynomial_features.fit_transform(x_pred)
	y_pred = model.predict(x_pred_transform)

	print(y_pred.flatten().tolist())
	plt.title("Variation in RSSI received vs distance from Bluetooth beacon ") 
	plt.xlabel("Distance in meters") 
	plt.ylabel("RSSI in dBm") 
	plt.plot(y_pred, x_pred, "-or")
	plt.plot(distance_list, rssi_list, "og")
	plt.show()

data_dir = os.getcwd() + "/beacon-original/"
f = open(os.path.join(data_dir, "beacon.json"),"r")
data = json.load(f)
f.close()

beacon_rssi_data = {}
beacon_distance_data = {}

for it in data["beacon"]:
	x_coord = it["x-coord"]
	y_coord = it["y-coord"]
	data_point = (x_coord, y_coord)
	beacon_rssi = {}
	beacon_distance = {}
	for reading in it["beaconData"]:
		beacon_rssi[reading["id3"]] = reading["rssi"]
		beacon_distance[reading["id3"]] = reading["distance"]
	beacon_rssi_data[data_point] = beacon_rssi
	beacon_distance_data[data_point] = beacon_distance

rssi_list_1 = []
rssi_list_3 = []
rssi_list_5 = []

distance_list_1 = []
distance_list_3 = []
distance_list_5 = []

for i in range(1, 60) :
	if i%2 == 0:
		data_point = (i, 1)
		if 1 in beacon_rssi_data[data_point] :
			rssi_list_1.append(beacon_rssi_data[data_point][1])
			distance_list_1.append(beacon_distance_data[data_point][1])
		data_point = (i, 5)
		if 1 in beacon_rssi_data[data_point] :
			rssi_list_5.append(beacon_rssi_data[data_point][1])
			distance_list_5.append(beacon_distance_data[data_point][1])
	else :
		data_point = (i, 3)
		if 1 in beacon_rssi_data[data_point] :
			rssi_list_3.append(beacon_rssi_data[data_point][1])
			distance_list_3.append(beacon_distance_data[data_point][1])

# values obtained from rss_estimator.py
fit_missing_distance(rssi_list_1, distance_list_1, 4, [-93.76550939984494, -93.73444212842611, -93.48592415265531, -93.0661869976001, -92.52817943777592, -91.93156749714603])
fit_missing_distance(rssi_list_3, distance_list_3, 4, [-96.02373560824489, -96.24537458861957, -96.18926588475158, -95.89496403746683, -95.41012253687545, -94.79049382237181])
fit_missing_distance(rssi_list_5, distance_list_5, 4, [-92.84848910911505, -93.12445400911051, -93.26254063114618, -93.29841186161869, -93.26753461767265, -93.20517984720072, -93.14642252884377])