# https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/utils/data_classes.py#L249

# 회전에 대한 좌표 변환 공식 : https://jangjy.tistory.com/267

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

# ex_folder = "C:\\Users\\wq_ysw\\Desktop\\Lidar\\07 ex_folder"
bin_path = "C:\\Users\\wq_ysw\\Desktop\\Lidar\\06 ex_file\\000000.bin"
label_path = "C:\\Users\\wq_ysw\\Desktop\\Lidar\\06 ex_file\\llab_000000.txt"

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


def read_bin_file(bin_path):
    size_float = 4
    list_pcd = []
    
    with open(bin_path, "rb") as f:
        byte = f.read(size_float * 4)
        while byte:
            x, y, z, intensity = struct.unpack("ffff", byte)
            list_pcd.append([x, y, z])
            byte = f.read(size_float * 4)
    return list_pcd


def readlines_label_file(label_path):
    label_list = []
    
    with open(label_path, "rt") as f:
        readlines_label = f.readlines()
        
        for label in readlines_label:
            label = label.split(" ")
            label = list(map(float, label))
            label_list.append(label)

        return label_list
    

def number_of_pointcloud_in_label(label_path, bin_path):    
    # 하나의 프레임에서 객체 안에 들어있는 point cloud 갯수를 구하고 있다.
    # 영역선 안에 들어있는 point cloud 갯수를 구하고 있다.

    list_pcd = read_bin_file(bin_path)
    label_list = readlines_label_file(label_path)
    result_dict = {}

    for label in label_list:
        # 객체 하나에 대한 for문.
        after_x1, after_x2, after_x3, after_x4, after_y1, after_y2, after_y3, after_y4, after_z_under, after_z_up = calculate_vertices(label)

        list_after_x = [after_x1, after_x2, after_x3, after_x4]
        list_after_y = [after_y1, after_y2, after_y3, after_y4]

        x_max_idx = list_after_x.index(max(list_after_x))
        x_min_idx = list_after_x.index(min(list_after_x))
        y_max_idx = list_after_y.index(max(list_after_y))
        y_min_idx = list_after_y.index(min(list_after_y))
        
        # print([after_x1, after_x2, after_x3, after_x4].index(max([after_x1, after_x2, after_x3, after_x4])), [after_y1, after_y2, after_y3, after_y4].index(max([after_y1, after_y2, after_y3, after_y4])))

        pcd_in_label = 0   # 하나의 레이블 영역 안에 들어 있는 pcd의 수, return 해야하는 값.
        pcd_in_range = []   # pcd_in_label을 구하기 전, 범위 안에 들어있는 pcd들을 담는 list로, pcd_in_label을 위해 for문을 돌려야하는 list

           
        # bounding box 안에 pcd가 있는지 확인하기 위한 직선의 기울기와 절편 
        gradient1, bias1 = calculate_gradient_and_bias(list_after_x[y_max_idx], list_after_y[y_max_idx], list_after_x[x_min_idx], list_after_y[x_min_idx])
        gradient2, bias2 = calculate_gradient_and_bias(list_after_x[x_max_idx], list_after_y[x_max_idx], list_after_x[y_max_idx], list_after_y[y_max_idx])
        gradient3, bias3 = calculate_gradient_and_bias(list_after_x[x_max_idx], list_after_y[x_max_idx], list_after_x[y_min_idx], list_after_y[y_min_idx])
        gradient4, bias4 = calculate_gradient_and_bias(list_after_x[y_min_idx], list_after_y[y_min_idx], list_after_x[x_min_idx], list_after_y[x_min_idx])
        

        
        for pcd in list_pcd:
            # pcd[pcd_z_idx] 값이 z-min과 z-max 사이에 있지 않으면 걸러야한다.
            # 변형된 x, y값 사이에 있지 않으면 걸러야한다.
            # x값을 입력했을 때, 4변에 해당하는 직선 사이에 있지 않으면 count 하면 안된다. 
            pcd_x = pcd[pcd_x_idx]
            pcd_y = pcd[pcd_y_idx]
            pcd_z = pcd[pcd_z_idx]
            
            

            #============================================
            if (min(list_after_x) < pcd_x) and (pcd_x < max(list_after_x)) and (min(list_after_y) < pcd_y) and (pcd_y < max(list_after_y)) and (after_z_under < pcd_z) and (pcd_z < after_z_up):
                pcd_in_range.append(pcd)
            #============================================
        # print(len(pcd_in_range))


        for pcd in pcd_in_range:
            # return 되는 값은 dictionary 형식으로 반환한다.

            if (pcd[pcd_y_idx] < gradient1 * pcd[pcd_x_idx] + bias1) and  (pcd[pcd_y_idx] < gradient2 * pcd[pcd_x_idx] + bias2) and (gradient4 * pcd[pcd_x_idx] + bias4 < pcd[pcd_y_idx]) and (gradient3 * pcd[pcd_x_idx] + bias3 < pcd[pcd_y_idx]):
                pcd_in_label = pcd_in_label + 1
                # print("asd")

        result_dict[label[tracking_id_idx]] = pcd_in_label

    return  result_dict

def calculate_vertices(label):
    # 회전된 x1, x2, x3, x4, y1, y2, y3, y4 꼭지점 구하기
    before_x1 = label[center_x_idx] + label[length_idx]/2
    before_x2 = label[center_x_idx] + label[length_idx]/2
    before_x3 = label[center_x_idx] + label[length_idx]/2 * -1
    before_x4 = label[center_x_idx] + label[length_idx]/2 * -1

    before_y1 = label[center_y_idx] + label[width_idx]/2
    before_y2 = label[center_y_idx] + label[width_idx]/2 * -1
    before_y3 = label[center_y_idx] + label[width_idx]/2 * -1
    before_y4 = label[center_y_idx] + label[width_idx]/2

    
    center_x = label[center_x_idx]
    center_y = label[center_y_idx]
    orientation = label[orientaion_idx]

    after_z_under = label[center_z_idx] - label[height_idx]/2
    after_z_up = label[center_z_idx] + label[height_idx]/2

    after_x1, after_y1 = rotate(before_x1, before_y1, center_x, center_y, orientation)
    after_x2, after_y2 = rotate(before_x2, before_y2, center_x, center_y, orientation)
    after_x3, after_y3 = rotate(before_x3, before_y3, center_x, center_y, orientation)
    after_x4, after_y4 = rotate(before_x4, before_y4, center_x, center_y, orientation)

    return after_x1, after_x2, after_x3, after_x4, after_y1, after_y2, after_y3, after_y4, after_z_under, after_z_up


def rotate(before_x, before_y, center_x, center_y, orientation):
    # 중점이 고려된 값이 나옴
    after_x = center_x + math.cos(orientation) * (before_x - center_x) - math.sin(orientation) * (before_y - center_y)
    after_y = center_y + math.sin(orientation) * (before_x - center_x) + math.cos(orientation) * (before_y - center_y)

    return after_x, after_y


def calculate_gradient_and_bias(x1, y1, x2, y2):
    # 사실 여기서 gradient는 math.tan()을 사용해도 된다.

    gradient = (y1 - y2)/(x1 - x2)
    bias = gradient * -1 * x1 + y1

    return gradient, bias



if __name__ == "__main__":
    start = time.time()
    result = number_of_pointcloud_in_label(label_path, bin_path)
    print(time.time()-start)
    print(result)
