import os
import shutil
import glob

ref_string = "25_26 19_18 25_2 7_2 25_18 19_26 13_2 13_40 25_34 13_34 13_10 1_2 7_34 1_10 19_40 19_2 1_34 1_40 25_40 7_40"
sample_string = "19_34 1_26 7_10 7_18 25_10 19_10 13_18 1_18 7_26 13_26"

ref_points_list = ref_string.split(" ")
sample_points_list = sample_string.split(" ")

for i in range(0, len(ref_points_list)) :
	ref_points_list[i] = "myReading_" + ref_points_list[i] + ".json"

for i in range(0, len(sample_points_list)) :
	sample_points_list[i] = "myReading_" + sample_points_list[i] + ".json"

final_readings_dir = os.getcwd() + "/final-readings/"
ref_points_readings_dir = os.getcwd() + "/ref-points-readings/"
sample_points_readings_dir = os.getcwd() + "/sample-points-readings/"

for filename in glob.glob(os.path.join(ref_points_readings_dir, '*.json')):
	with open(filename, 'r') as f:
		os.remove(filename)

for filename in glob.glob(os.path.join(sample_points_readings_dir, '*.json')):
	with open(filename, 'r') as f:
		os.remove(filename)

for filename in glob.glob(os.path.join(final_readings_dir, '*.json')):
	with open(filename, 'r') as f:
		ff = filename.split('/')
		fl_name = ff[-1]

		if fl_name in ref_points_list :
			fl_name = ref_points_readings_dir + fl_name
			shutil.copy(filename, fl_name)
		else :
			fl_name = sample_points_readings_dir + fl_name
			shutil.copy(filename, fl_name)