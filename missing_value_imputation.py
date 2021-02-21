import json
import os
import glob
import random

b1 = {}
b2 = {}
ref_dir = os.getcwd() + "/beaconRef-original/"
f = open(os.path.join(ref_dir, "beaconRef.json"),"r")
data = json.load(f)
f.close()

for it in data["beaconRef"]:
	x_coord = it["x-coord"]
	y_coord = it["y-coord"]
	ref_point = (x_coord, y_coord)
	beacon_data = {}
	beacon_distance = {}
	for reading in it["beaconData"]:
		beacon_data[reading["address"]] = reading["rssi"]
		beacon_distance[reading["address"]] = reading["distance"]
	b1[ref_point] = beacon_data
	b2[ref_point] = beacon_distance

my_list = []
dist_list = []

for i in range(1,60) :
	if i%2 == 0:
		ref_point = (i, 1)
		if "0C:F3:EE:B5:B3:B9" in b1[ref_point] :
			my_list.append(b1[ref_point]["0C:F3:EE:B5:B3:B9"])
			dist_list.append(b2[ref_point]["0C:F3:EE:B5:B3:B9"])
		else :
			my_list.append(0)
			dist_list.append(0)
		ref_point = (i, 5)
		if "0C:F3:EE:B5:B3:B9" in b1[ref_point] :
			my_list.append(b1[ref_point]["0C:F3:EE:B5:B3:B9"])
			dist_list.append(b2[ref_point]["0C:F3:EE:B5:B3:B9"])
		else :
			my_list.append(0)
			dist_list.append(0)
	else :
		ref_point = (i, 3)
		if "0C:F3:EE:B5:B3:B9" in b1[ref_point] :
			my_list.append(b1[ref_point]["0C:F3:EE:B5:B3:B9"])
			dist_list.append(b2[ref_point]["0C:F3:EE:B5:B3:B9"])
		else :
			my_list.append(0)
			dist_list.append(0)


print(my_list)
print()
print(dist_list)
print()

list2 = my_list[34:44] + my_list[63:73]
print(list2)
print()

print(sum(list2)/len(list2))
print(max(list2))
print(min(list2))

print()
list3 = dist_list[34:44] + dist_list[63:73]
print(list3)
print()
print(sum(list3)/len(list3))
print(max(list3))
print(min(list3))