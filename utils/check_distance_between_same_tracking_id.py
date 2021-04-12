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

tracking_id_idx = 0
type_idx = 1
center_x_idx = 2
center_y_idx = 3
center_z_idx = 4
length_idx = 5
width_idx = 6
height_idx = 7
orientaion_idx = 8
det_diff_level_idx = 9

pcd_x_idx = 0
pcd_y_idx = 1
pcd_z_idx = 2

def change_type_in_label(label):
    new_type_label = []
    new_type_label.append(label[0])
    new_type_label.append(label[1])
    new_type_label.append(float(label[2]))
    new_type_label.append(float(label[3]))
    new_type_label.append(float(label[4]))
    new_type_label.append(float(label[5]))
    new_type_label.append(float(label[6]))
    new_type_label.append(float(label[7]))
    new_type_label.append(float(label[8]))
    new_type_label.append(label[9])

    return new_type_label

def readlines_label_file(label_path):
    label_list = []
    
    with open(label_path, "rt") as f:
        readlines_label = f.readlines()
        
        for label in readlines_label:
            label = label.split(" ")
            label = change_type_in_label(label)
            label_list.append(label)

        return label_list

def check_distance_between_same_tracking_id(same_before_label, same_label, threshold):
    # 전 프레임과 비교해서 같은 tracking_id 인데 거리가 threshold 보다 큰지 아닌지 확인하는 함수
    distance = math.sqrt(pow((same_before_label[center_x_idx] - same_label[center_x_idx]), 2) + pow((same_before_label[center_y_idx] - same_label[center_y_idx]), 2) + pow((same_before_label[center_z_idx] - same_label[center_z_idx]), 2))

    if threshold < distance:
        return True # True라는 것은 전 프레임과 비교해서 같은 tracking_id 인데 거리가 threshold 보다 크다는 것을 의미함