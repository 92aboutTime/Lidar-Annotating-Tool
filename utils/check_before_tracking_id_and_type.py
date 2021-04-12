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

def check_before_tracking_id_and_type(before_label_list, label_list):
    # 전 프레임와 비교해서 같은 tracking_id 임에도 불구하고 type가 다른 경우를 확인하는 함수
    # 같은 프레임 내에 동일한 tracking_id는 없다는 가정으로 진행
    result_dict = {}
    
    for label in label_list:
        for before_label in before_label_list:
            if label[tracking_id_idx] == before_label[tracking_id_idx] and label[type_idx] != before_label[type_idx]:
                result_dict[label[tracking_id_idx]] = True # 전 프레임과 type이 다르다는 것이 True

    return result_dict
