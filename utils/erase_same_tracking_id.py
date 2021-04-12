import os
import shutil
from tqdm import tqdm
import pandas as pd
import sys

# ssd_dan_path = 'C:\\Users\\wq_ysw\\Desktop\\Lidar\\03 소스코드\\ex_folder\\dan\\'
# ssd_jeon_path = 'C:\\Users\\wq_ysw\\Desktop\\Lidar\\03 소스코드\\ex_folder\\jeon\\'

# file_path = 'C:\\Users\\wq_ysw\\Desktop\\Lidar\\03 소스코드\\ex_file\\llab_000000.txt'
# file_test = 'C:\\Users\\wq_ysw\\Desktop\\Lidar\\03 소스코드\\ex_file\\1.txt'

# path = 'C:\\Users\\wq_ysw\\Desktop\\Lidar\\07 ex_folder'

def erase_same_tracking_id(path, dan_or_jeon, folder):
    path_label = os.path.join(path, dan_or_jeon ,folder,'lidar','lidar_label')
    
    try:
        label_list = sorted(os.listdir(path_label))
    except:
        print("{} lidar_label folder 없음".format(folder))
        # return

    for i in label_list:
        readlines_erase(os.path.join(path_label, i))
            
            
def readlines_erase(file_path):
    with open(file_path, mode = 'r', encoding = 'utf-8') as label:
        lines = label.readlines()
        list_lines = sorted(list(set(lines)))     

    with open(file_path, mode = 'w', encoding = 'utf-8') as label:
        label.write("")

    with open(file_path, mode = 'a', encoding = 'utf-8') as label: 
        for line in list_lines:
            label.write(line)
        
# erase_same_tracking_id(path, "jeon", "2020-11-27-13-35-29-04")

if __name__ == "__main__":
    path = "X:\\"
    dan_or_jeon = 'jeon'

    dan_or_jeon_list = sorted(os.listdir(os.path.join(path, dan_or_jeon)))
    print(len(dan_or_jeon_list))

    for folder in tqdm(dan_or_jeon_list):
        print(folder)
        erase_same_tracking_id(path, dan_or_jeon, folder)
