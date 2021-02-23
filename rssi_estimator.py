from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
import numpy as np 
from matplotlib import pyplot as plt 
import json
import os

def fit_missing_rssi(x_list, rssi_list, poly_degree, x_pred_list) :
	x = np.array(x_list)
	X = x.reshape(-1, 1)
	y = np.array(rssi_list)
	Y = y.reshape(-1, 1)

	polynomial_features = PolynomialFeatures(degree=poly_degree)
	x_poly = polynomial_features.fit_transform(X)

	model = LinearRegression()
	model.fit(x_poly, Y)

	x_pred = np.array(x_pred_list).reshape(-1,1)
	x_pred_transform = polynomial_features.fit_transform(x_pred)
	y_pred = model.predict(x_pred_transform)

	print(y_pred.flatten().tolist())
	plt.plot(x_pred, y_pred, "-or")
	plt.plot(x_list, rssi_list, "og")
	plt.show()

ref_dir = os.getcwd() + "/beaconRef-original/"
f = open(os.path.join(ref_dir, "beaconRef.json"),"r")
data = json.load(f)
f.close()

b1 = {}

for it in data["beaconRef"]:
	x_coord = it["x-coord"]
	y_coord = it["y-coord"]
	ref_point = (x_coord, y_coord)
	beacon_rssi = {}
	for reading in it["beaconData"]:
		beacon_rssi[reading["id3"]] = reading["rssi"]
	b1[ref_point] = beacon_rssi

x_list_1 = []
x_list_3 = []
x_list_5 = []

rssi_list_1 = []
rssi_list_3 = []
rssi_list_5 = []

for i in range(1,60) :
	if i%2 == 0:
		ref_point = (i, 1)
		if 1 in b1[ref_point] :
			rssi_list_1.append(b1[ref_point][1])
			x_list_1.append(i)
		ref_point = (i, 5)
		if 1 in b1[ref_point] :
			rssi_list_5.append(b1[ref_point][1])
			x_list_5.append(i)
	else :
		ref_point = (i, 3)
		if 1 in b1[ref_point] :
			rssi_list_3.append(b1[ref_point][1])
			x_list_3.append(i)

# x_list_1 should be equal to [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 44, 46, 48, 50, 52, 54, 56, 58]
# x_list_3 should be equal to [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 43, 45, 47, 49, 51, 53, 55, 57, 59]
# x_list_5 should be equal to [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 44, 46, 48, 50, 52, 54, 56, 58]

fit_missing_rssi(x_list_1, rssi_list_1, 4, [32, 34, 36, 38, 40, 42])
fit_missing_rssi(x_list_3, rssi_list_3, 4, [31, 33, 35, 37, 39, 41])
fit_missing_rssi(x_list_5, rssi_list_5, 4, [30, 32, 34, 36, 38, 40, 42])