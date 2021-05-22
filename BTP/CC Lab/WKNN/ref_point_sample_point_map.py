import numpy as np 
from matplotlib import pyplot as plt 
import json
import os

noOfTilesX = 19
noOfTilesY = 19

ref_x_list = []
ref_y_list = []
sample_x_list = []
sample_y_list = []

save_path = os.getcwd() + "/Graphs/ref_point_sample_point/"
if not(os.path.isdir(save_path)) : 
	os.mkdir(save_path)

ref_dir = os.getcwd() + "/beacon-ref-points-raw/"
f = open(os.path.join(ref_dir, "beacon.json"), "r")
data = json.load(f)
f.close()

for item in data["beacon"] :
	ref_x_list.append(item["x-coord"])
	ref_y_list.append(item["y-coord"])

sample_dir = os.getcwd() + "/beacon-sample-points-raw/"
f = open(os.path.join(sample_dir, "beacon.json"), "r")
data = json.load(f)
f.close()

for item in data["beacon"] :
	sample_x_list.append(item["x-coord"])
	sample_y_list.append(item["y-coord"])

label = {}

for i in range(0, len(ref_x_list)) :
	x_coord = ref_x_list[i]
	y_coord = ref_y_list[i]
	data_point = (x_coord, y_coord)
	label[data_point] = 1

for i in range(0, len(sample_x_list)) :
	x_coord = sample_x_list[i]
	y_coord = sample_y_list[i]
	data_point = (x_coord, y_coord)
	label[data_point] = 0

w, h = noOfTilesY, noOfTilesX;
Matrix = [[np.NaN for x in range(w)] for y in range(h)]

for data_point in label :
	Matrix[data_point[0]//2][data_point[1]//2] = label[data_point]

rssi_map = np.array(Matrix)
plt.figure(figsize=(16, 10))
# plt.title("Signal strength map (discrete) of beacon " + str(beaconNo) + " located at (" + str(10*beaconNo-5) + ", " + str(0 if beaconNo%2==1 else 6) + ")\n")
plt.yticks([i for i in range(1, h+1)])
plt.xticks([i for i in range(1, w+1)])
plt.imshow(rssi_map, cmap='hot', interpolation='nearest', extent=[0,w,h,0])
plt.colorbar(orientation='horizontal')
plt.clim(0, 2)
# plt.show()
filename = os.path.join(save_path, "ref_point_sample_point")
plt.savefig(filename, dpi=200, bbox_inches='tight')
plt.close()