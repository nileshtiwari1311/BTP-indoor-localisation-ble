from matplotlib import pyplot as plt 
import json
import os

ref_dir = os.getcwd() + "/final-readings/"
f = open(os.path.join(ref_dir, "myReading_9_3.json"),"r")
data = json.load(f)
f.close()

save_dir = os.getcwd() + "/Graphs/rssi_vs_sampling_times/"
if not(os.path.isdir(save_dir)) : 
	os.mkdir(save_dir)

rssi_dict = {}

for sample in data["beaconReadings"] :
	for reading in sample["readings"] :
		if reading["id3"] in rssi_dict:
			rssi_dict[reading["id3"]].append(reading["rssi"])
		else :
			rssi_dict[reading["id3"]] = [reading["rssi"]]

plt.figure(figsize=(16, 10))
plt.title("Raw RSSI vs Sampling times")
plt.xlabel("Sampling times") 
plt.ylabel("RSSI in dBm")
plt.plot([x for x in range(1, len(rssi_dict[1])+1)], rssi_dict[1], "-ob")
plt.plot([x for x in range(1, len(rssi_dict[3])+1)], rssi_dict[3], "-og")
plt.plot([x for x in range(1, len(rssi_dict[5])+1)], rssi_dict[5], "-om")
plt.legend(["beacon 1","beacon 3","beacon 5"])
# plt.show()
filename = os.path.join(save_dir, "rssi_vs_sampling_times_9_3_odd")
plt.savefig(filename, dpi=200, bbox_inches='tight')
plt.close()

plt.figure(figsize=(16, 10))
plt.title("Raw RSSI vs Sampling times")
plt.xlabel("Sampling times") 
plt.ylabel("RSSI in dBm")
plt.plot([x for x in range(1, len(rssi_dict[2])+1)], rssi_dict[2], "-or")
plt.plot([x for x in range(1, len(rssi_dict[4])+1)], rssi_dict[4], "-oc")
plt.plot([x for x in range(1, len(rssi_dict[6])+1)], rssi_dict[6], "-oy")
plt.legend(["beacon 2","beacon 4","beacon 6"])
# plt.show()
filename = os.path.join(save_dir, "rssi_vs_sampling_times_9_3_even")
plt.savefig(filename, dpi=200, bbox_inches='tight')
plt.close()