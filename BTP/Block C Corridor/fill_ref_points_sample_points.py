import os
import shutil
import glob

ref_string = "32_5 10_1 10_5 12_5 13_3 14_1 14_5 15_3 16_1 19_3 1_3 20_5 22_5 23_3 24_5 25_3 29_3 34_5 39_3 3_3 44_1 45_3 46_1 46_5 47_3 48_1 48_5 49_3 4_1 4_5 50_1 52_1 52_5 54_1 55_3 56_1 56_5 57_3 58_1 58_5 59_3 5_3 6_5 7_3 8_1"
sample_string = "30_1 11_3 12_1 16_5 17_3 18_1 18_5 20_1 21_3 22_1 24_1 26_1 26_5 27_3 28_1 28_5 2_1 2_5 30_5 31_3 32_1 33_3 34_1 35_3 36_1 36_5 37_3 38_1 38_5 40_1 40_5 41_3 42_1 42_5 43_3 44_5 50_5 51_3 53_3 54_5 6_1 8_5 9_3"

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