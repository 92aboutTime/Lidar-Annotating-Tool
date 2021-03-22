#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import os
import sys
from tqdm import tqdm
import shutil

# ssd_path = "/volumeUSB1/usbshare1-1/"
# volume1_path = "/volume1/가공완료데이터/"
csv_path = "C:\\Users\\wq_ysw\\Desktop\\Lidar\\02 엑셀 파일\\김소현브로 재검수.xlsx"

volume1_path = "X:\\"
ssd_path = "V:\\"

column = "검수자"
name = "문현경"

def eggORzip(x):
    if '.egg' in x:
        return x.split('.egg')[0]
    elif '.zip' in x:
        return x.split('.zip')[0]

def read_csv_path(csv_path, column, name):
    df = pd.read_excel(csv_path, sheet_name = '재검수')
    df = df[df[column] == name]
    
    df_new = pd.DataFrame(columns = ['No', '파일','검수완료_옮김_유무', '단방향', '전방향']) 
    df_new['파일'] = df['파일명'].apply(lambda x : eggORzip(x))
    df_new['No'] = df['No']
    df_new['단방향'] = df['단방향']
    df_new['전방향'] = df['전방향']
    df_new['검수완료_옮김_유무'] = df['검수완료_옮김_유무']
    return df_new

def move_sw_file_to_nas(csv_path, column, name, dan_or_jeon):
    ssd_folder_path = os.path.join(ssd_path, dan_or_jeon)
    ssd_folder_list = sorted(os.listdir(ssd_folder_path))

    if dan_or_jeon == "dan":
        column_for_dan_or_jeon = "단방향"
    if dan_or_jeon == "jeon":
        column_for_dan_or_jeon = "전방향"

    df_new = read_csv_path(csv_path, column, name)

    for filename in tqdm(df_new[(df_new[column_for_dan_or_jeon]==True) & (df_new['검수완료_옮김_유무']==False)]['파일']):
        
        if filename in ssd_folder_list:
            ssd_path_dan_label = os.path.join(ssd_folder_path, filename, 'lidar\\lidar_label')
            obj_path = os.path.join(volume1_path, dan_or_jeon, filename, 'lidar\\lidar_label')
            print(ssd_path_dan_label)
            print(obj_path)
            print("\n")
            
            shutil.rmtree(obj_path)
            shutil.copytree(ssd_path_dan_label, obj_path)
        

if __name__ == "__main__":
    move_sw_file_to_nas(csv_path, column, name, "jeon")