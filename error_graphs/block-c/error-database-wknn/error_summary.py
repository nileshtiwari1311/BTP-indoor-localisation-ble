import os
import json
from matplotlib import pyplot as plt

f = open("beacon_error_database_complete.json")
data = json.load(f)
f.close()

error_list = sorted(data["values"], key = lambda i: i['mae-ble'])
for i in range(10) :
	print(error_list[i])