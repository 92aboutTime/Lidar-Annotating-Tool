#!/usr/bin/env python
# coding: utf-8
import os
import shutil
from tqdm import tqdm
import sys
import pandas as pd

def check_error_file(folder, dan_or_jeon):
    folder_path = os.path.join("X:\\", dan_or_jeon, folder, "lidar\\lidar_label")
    # print(folder_path)

    folder_list = os.listdir(folder_path)
    result_list = []

    for label_name in folder_list:
        # print(label_name)
        label_path = os.path.join(folder_path, label_name)
        
        if os.path.getsize(label_path) != 0 : 

            with open(label_path, mode = 'rt', encoding = 'utf-8') as label:
                
                lines = label.readlines()

                for line in lines:
                    if line.count(" ") != 9 and not "sts_" in line:
                        result_list.append([folder, label_name, False])
                    elif line.count(" ") != 9 and "sts_" in line:
                        result_list.append([folder, label_name, True])

    return result_list
                    




if __name__ == "__main__":

    dan_path = "X:\\dan"
    jeon_path = "X:\\jeon"

    dan_list = sorted(os.listdir(dan_path))
    jeon_list = sorted(os.listdir(jeon_path))

    a = 0
    df = pd.DataFrame(columns = ['폴더', 'label_번호', 'sts_문제'])

    j = 0
    for dan in dan_list:
        if a != 2:
            result_list = check_error_file(dan, "dan")
            
            if result_list != None:
                for result in result_list:
                    df.loc[j] = result
                    j = j + 1
            
            a = a + 1

df.to_csv('C:\\Users\\wq_ysw\\Desktop\\Lidar\\file_error_단방향.csv', mode='w', index=False, encoding='utf-8-sig')