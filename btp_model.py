import json
import os
import glob

m1 = {}
ref_dir = os.getcwd() + "/geoMagRef-model/"
f = open(os.path.join(ref_dir, "geoMagRef.json"),"r")
data = json.load(f)
f.close()

#map<pair<x,y>,<mx,my,mz,MA>> m1;

for it in data["geoMagRef"]:
	x_coord = it["x-coord"]
	y_coord = it["y-coord"]
	ref_point = (x_coord, y_coord)
	m1[ref_point] = (it['mx'], it['my'], it['mz'], it["MA"])

b1 = {}
ref_dir = os.getcwd() + "/beaconRef-model/"
f = open(os.path.join(ref_dir, "beaconRef.json"),"r")
data = json.load(f)
f.close()

for it in data["beaconRef"]:
	x_coord = it["x-coord"]
	y_coord = it["y-coord"]
	ref_point = (x_coord, y_coord)
	beacon_data = {}
	for reading in it["beaconData"]:
		beacon_data[reading["address"]] = reading["rssi"]
	b1[ref_point] = beacon_data

print("Expected\t\tGeoMag\t\t\tBLE")
sample_dir = os.getcwd() + "/sample-points-readings/"
for filename in glob.glob(os.path.join(sample_dir, '*.json')):
	with open( filename, 'r') as f: 

		m2 = {}
		#map<pair<x,y>, D > m2; where D is w

		data = json.load(f)
		f.close()
		x_coord = data["x-coord"]
		y_coord = data["y-coord"]
		mag_data_len = len(data["geoMagReadings"])
		
		mx = 0
		my = 0
		mz = 0
		MA = 0
		for i in range(0,mag_data_len):
			mx+=data["geoMagReadings"][i]["mx"]
			my+=data["geoMagReadings"][i]["my"]
			mz+=data["geoMagReadings"][i]["mz"]
			MA+=data["geoMagReadings"][i]["MA"]

		mx/=mag_data_len
		my/=mag_data_len
		mz/=mag_data_len
		MA/=mag_data_len

		for jt in m1:
			dx = m1[jt][0] - mx
			dy = m1[jt][1] - my
			dz = m1[jt][2] - mz
			DA = m1[jt][3] - MA
			val = (dx*dx) + (dy*dy) + (dz*dz) + (DA*DA)
			val/=4
			val = val**(0.5)
			m2[jt] = val

		x_mag = 0
		divi=0
		y_mag = 0
		for jt in m2:
			if m2[jt] == 0:
				m2[jt] = 0.001
			x_mag+=(jt[0]/m2[jt])
			divi+=(1/m2[jt])
			y_mag+=(jt[1]/m2[jt])

		x_mag/= divi
		y_mag/= divi

		beacon_data_len = len(data["beaconReadings"])
		beacon_data = {}

		for i in range(0, beacon_data_len) :
			for reading in data["beaconReadings"][i]["readings"] :
				rssi = reading["rssi"]
				id3 = reading["id3"]
				address = reading["address"]
				if address in beacon_data :
					beacon_data[address]["count"]+=1
					beacon_data[address]["rssi"]+=rssi
				else :
					beacon_data[address] = {"count" : 1, "rssi" : rssi, "id3" : id3}

		for address in beacon_data:
			beacon_data[address] = beacon_data[address]["rssi"]/beacon_data[address]["count"]
		
		b2 = {}
		for jt in b1 :
			val = 0
			for address in b1[jt] :
				val += (b1[jt][address] - beacon_data[address])**2

			b2[jt] = (val)**(0.5)

		x_ble = 0
		divi=0
		y_ble = 0
		for jt in b2:
			if b2[jt] == 0:
				b2[jt] = 0.001
			x_ble+=(jt[0]/b2[jt])
			divi+=(1/b2[jt])
			y_ble+=(jt[1]/b2[jt])

		x_ble/= divi
		y_ble/= divi

		print("x=" + str(x_coord) + "\t\tx=" + str(x_mag) + "\t\tx=" + str(x_ble))
		print("y=" + str(y_coord) + "\t\ty=" + str(y_mag) + "\t\ty=" + str(y_ble))
		print()