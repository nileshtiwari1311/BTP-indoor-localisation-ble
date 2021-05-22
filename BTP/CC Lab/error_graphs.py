import os
import json
from matplotlib import pyplot as plt

n = 10

save_path = os.getcwd() + "/Graphs/"
if not(os.path.isdir(save_path)) : 
	os.mkdir(save_path)

# candlestick
# wknn
data_dir = os.getcwd() + "/WKNN/error-database/"
f = open(os.path.join(data_dir, "beacon_error_database_complete.json"), "r")
data = json.load(f)
f.close()

error_list = sorted(data["values"], key = lambda i: i['mae-ble'])

fd = error_list[0]["fd"]
k = error_list[0]["k"]
filterMethod = error_list[0]["filter"]

mae_list = [0 for i in range(3, n+1)]
min_err_list = [0 for i in range(3, n+1)]
max_err_list = [0 for i in range(3, n+1)]

for item in data["values"] :
	if item["k"] == k and item["filter"] == filterMethod :
		mae_list[item["fd"]-3] = item["mae-ble"]
		min_err_list[item["fd"]-3] = item["min-error-ble"]
		max_err_list[item["fd"]-3] = item["max-error-ble"]

# plot the candlestick graph
for i in range(3, n+1) :
	plt.vlines(x=i, ymin=min_err_list[i-3], ymax=max_err_list[i-3])
	plt.plot(i, min_err_list[i-3], "og")
	plt.plot(i, mae_list[i-3], "oy")
	plt.plot(i, max_err_list[i-3], "or")
plt.plot([i for i in range(3, n+1)], mae_list, "-y")
plt.ylabel("Error (m)", fontsize=15)
plt.xlabel("Fingerprint Dimensionality", fontsize=15)
plt.legend(["Minimum Error", "Mean Error", "Maximum Error"])
plt.xticks([i for i in range(3, n+1)])
plt.grid()
# plt.show()
filename = os.path.join(save_path, "candlestick_cc_wknn")
plt.savefig(filename, dpi=200, bbox_inches='tight')
plt.close()

#nlls
data_dir = os.getcwd() + "/NLLS/error-database/"
f = open(os.path.join(data_dir, "beacon_error_database_complete.json"), "r")
data = json.load(f)
f.close()

error_list = sorted(data["values"], key = lambda i: i['mae-ble'])

fd = error_list[0]["fd"]
filterMethod = error_list[0]["filter"]

mae_list = [0 for i in range(3, n+1)]
min_err_list = [0 for i in range(3, n+1)]
max_err_list = [0 for i in range(3, n+1)]

for item in data["values"] :
	if item["filter"] == filterMethod :
		mae_list[item["fd"]-3] = item["mae-ble"]
		min_err_list[item["fd"]-3] = item["min-error-ble"]
		max_err_list[item["fd"]-3] = item["max-error-ble"]

# plot the candlestick graph
for i in range(3, n+1) :
	plt.vlines(x=i, ymin=min_err_list[i-3], ymax=max_err_list[i-3])
	plt.plot(i, min_err_list[i-3], "og")
	plt.plot(i, mae_list[i-3], "oy")
	plt.plot(i, max_err_list[i-3], "or")
plt.plot([i for i in range(3, n+1)], mae_list, "-y")
plt.ylabel("Error (m)", fontsize=15)
plt.xlabel("Fingerprint Dimensionality", fontsize=15)
plt.legend(["Minimum Error", "Mean Error", "Maximum Error"])
plt.xticks([i for i in range(3, n+1)])
plt.grid()
# plt.show()
filename = os.path.join(save_path, "candlestick_cc_nlls")
plt.savefig(filename, dpi=200, bbox_inches='tight')
plt.close()

# cdf
# wknn
data_dir = os.getcwd() + "/WKNN/error-database/"
f = open(os.path.join(data_dir, "beacon_error_database_complete.json"), "r")
data = json.load(f)
f.close()

error_list = sorted(data["values"], key = lambda i: i['mae-ble'])

fd = error_list[0]["fd"]
k = error_list[0]["k"]
filterMethod = error_list[0]["filter"]

f = open(os.path.join(data_dir, "beacon_error_database_" + filterMethod + "_k" + str(k) + "_fd" + str(fd) + ".json"), "r")
data = json.load(f)
f.close()

error_coord_list = []
for item in data["error-coord"] :
	error_coord_list.append(round(item["err-ble"], 2))

error_coord_list = sorted(error_coord_list)
num = len(error_coord_list)

probability_list_wknn = [0.0]
distance_list_wknn = [0.0]
count = 0

for error_coord in error_coord_list :
	count += 1
	distance_list_wknn.append(error_coord)
	probability_list_wknn.append(round(count/num, 2))

# nlls
data_dir = os.getcwd() + "/NLLS/error-database/"
f = open(os.path.join(data_dir, "beacon_error_database_complete.json"), "r")
data = json.load(f)
f.close()

error_list = sorted(data["values"], key = lambda i: i['mae-ble'])

fd = error_list[0]["fd"]
filterMethod = error_list[0]["filter"]

f = open(os.path.join(data_dir, "beacon_error_database_" + filterMethod + "_fd" + str(fd) + ".json"), "r")
data = json.load(f)
f.close()

error_coord_list = []
for item in data["error-coord"] :
	error_coord_list.append(round(item["err-ble"], 2))

error_coord_list = sorted(error_coord_list)
num = len(error_coord_list)

probability_list_nlls = [0.0]
distance_list_nlls = [0.0]
count = 0

for error_coord in error_coord_list :
	count += 1
	distance_list_nlls.append(error_coord)
	probability_list_nlls.append(round(count/num, 2))

max_d = max([distance_list_nlls[-1], distance_list_wknn[-1]])
print(max_d)

plt.xlabel('Error(m)', fontsize=15)
plt.ylabel('Cumulative Probability', fontsize=15)
plt.yticks([x/10 for x in range(11)])
plt.xlim([0.0, max_d+0.1])
plt.ylim([0.0, 1.1])
plt.plot(distance_list_wknn, probability_list_wknn, "-b")
plt.plot(distance_list_nlls, probability_list_nlls, "-r")
plt.legend(["WKNN", "NLLS"], fontsize=15)
plt.grid()
# plt.show()
filename = os.path.join(save_path, "cdf_cc")
plt.savefig(filename, dpi=200, bbox_inches='tight')
plt.close()