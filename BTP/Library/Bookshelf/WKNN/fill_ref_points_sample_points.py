import os
import shutil
import glob

ref_string = "23_53 27_57 1_49 1_57 13_57 27_45 9_57 27_53 5_57 9_45 1_45 13_45 27_49 5_45"
sample_string = "9_53 17_53 5_53 13_53 17_57 9_49 5_49 13_49 17_49 23_45 23_49 23_57 1_53 17_45"

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