import os
import shutil
import glob

ref_string = "31_23 11_1 11_37 15_15 15_3 15_33 15_9 19_29 19_35 23_1 23_37 27_21 27_3 27_33 27_9 31_11 31_17 31_29 31_35 31_5 35_1 35_13 35_19 35_37 35_7 3_15 3_21 3_27 3_3 3_33 3_9 7_11 7_23 7_35"
sample_string = "11_13 11_19 11_25 11_31 11_7 15_21 15_27 19_11 19_17 19_23 19_5 23_13 23_19 23_25 23_31 23_7 27_15 27_27 35_25 35_31 7_17 7_29 7_5"

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