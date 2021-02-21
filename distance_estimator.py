from sklearn import gaussian_process
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel
import numpy as np 
from matplotlib import pyplot as plt 
import json
import os
import glob

ref_dir = os.getcwd() + "/beaconRef-original/"
f = open(os.path.join(ref_dir, "beaconRef.json"),"r")
data = json.load(f)
f.close()

distance = {}
rssi = {}


for elem in data["beaconRef"]:
	for values in elem["beaconData"]:
		if values["id3"] in distance :
			distance[values["id3"]].append(values["distance"])
		else :
			distance[values["id3"]] = [values["distance"]]

		if values["id3"] in rssi :
			rssi[values["id3"]].append(values["rssi"])
		else :
			rssi[values["id3"]] = [values["rssi"]]
		

x = np.array(rssi[1])
X = x.reshape(-1, 1)
y = np.array(distance[1])
Y = y.reshape(-1, 1)


kernel = ConstantKernel() + Matern(length_scale=2, nu=3/2) + WhiteKernel(noise_level=1)
#GaussianProcessRegressor(alpha=1e-10, copy_X_train=True, kernel=1**2 + Matern(length_scale=2, nu=1.5) + WhiteKernel(noise_level=1), n_restarts_optimizer=0, normalize_y=False, optimizer='fmin_l_bfgs_b', random_state=None)

gp = gaussian_process.GaussianProcessRegressor(kernel=kernel)
gp.fit(X, Y)

x_pred = np.linspace(-96, -89).reshape(-1,1)
y_pred, sigma = gp.predict(x_pred, return_std=True)

plt.title("Variation in RSSI received vs distance from Bluetooth beacon ") 
plt.xlabel("Distance in meters") 
plt.ylabel("RSSI in dBm") 
plt.plot(y_pred, x_pred, "ob")  
plt.show()