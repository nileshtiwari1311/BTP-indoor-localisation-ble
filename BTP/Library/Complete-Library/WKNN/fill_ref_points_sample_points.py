import os
import shutil
import glob

ref_string = "23_53 9_53 27_57 25_26 17_53 1_49 5_53 25_2 1_57 13_53 13_57 17_57 25_18 19_26 5_49 13_2 9_57 27_53 17_49 13_10 1_2 19_2 25_10 19_10 1_34 1_40 13_18 27_49 1_18 7_26 1_53 13_26"
sample_string = "19_34 19_18 7_2 27_45 9_49 1_26 7_10 13_40 25_34 13_34 13_49 5_57 7_18 23_45 23_49 9_45 7_34 1_10 1_45 13_45 19_40 23_57 25_40 7_40 5_45 17_45"

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