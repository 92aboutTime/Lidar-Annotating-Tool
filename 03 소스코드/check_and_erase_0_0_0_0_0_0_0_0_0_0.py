import pandas as pd
import numpy as np
import os
import sys
from tqdm import tqdm
import shutil
import open3d as o3d
import struct
import math
import time

dan_path = "X:\\dan"
jeon_path = "X:\\jeon"

dan_list = sorted(os.listdir(dan_path))
jeon_list = sorted(os.listdir(jeon_path))

tracking_id_idx = 0
type_idx = 1
center_x_idx = 2
center_y_idx = 3
center_z_idx = 4
length_idx = 5
width_idx = 6
height_idx = 7
orientation_idx = 8
det_diff_level_idx = 9

def check_0_0_0_0_0_0_0_0_0_0(lines):
    del_i_list = []

    for i, line in enumerate(lines):
        if line.split(" ")[length_idx : orientation_idx] == ['0', '0', '0'] :
            del lines[i]
            i = i - 1
    return lines

def erase_0_0_0_0_0_0_0_0_0_0(file_path):
    with open(file_path, mode = 'r', encoding = 'utf-8') as label:
        lines = label.readlines()
        list_lines = check_0_0_0_0_0_0_0_0_0_0(lines)     

    with open(file_path, mode = 'w', encoding = 'utf-8') as label:
        label.write("")

    with open(file_path, mode = 'a', encoding = 'utf-8') as label: 
        for line in list_lines:
            label.write(line)



if __name__ == "__main__":

    # path = "F:\\0_0_0"
    path = jeon_path
    path_list = sorted(os.listdir(path))

    for folder in tqdm(path_list):
        path_lidar = os.path.join(path, folder, "lidar", "lidar_label")
        lidar_list = sorted(os.listdir(path_lidar))
        
        for lidar_path in lidar_list:
            file_path = os.path.join(path_lidar, lidar_path)
            erase_0_0_0_0_0_0_0_0_0_0(file_path)
            