#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import shutil
from tqdm import tqdm
import sys

YMA = sys.argv[1]
dan = sys.argv[2]
jeon = sys.argv[3]

U_dan_path = '/volume1/가공완료데이터/dan'
U_jeon_path = '/volume1/가공완료데이터/jeon'

W_dan_path = os.path.join('/volume1/가공완료데이터-영상비식별화',YMA,dan)
W_jeon_path = os.path.join('/volume1/가공완료데이터-영상비식별화',YMA,jeon)

if os.path.isdir(W_dan_path):
    W_dan_list = os.listdir(W_dan_path)
    W_dan_list = sorted(W_dan_list)

    for i, folder in enumerate(tqdm(W_dan_list)) :
        if folder.count('-') < 6:
            continue
        else :
            i = i+1
            
            dan_before_path = os.path.join(W_dan_path, folder, 'lidar', 'lidar_label')
            dan_obj_path = os.path.join(U_dan_path, folder, 'lidar', 'lidar_label')
            
            print('{}번째_단방향: {}'.format(i,dan_before_path))
            print('{}번째_단방향: {}\n'.format(i, dan_obj_path))
            
            if os.path.isdir(dan_before_path):
                shutil.rmtree(dan_before_path)
            
            if not os.path.isdir(dan_obj_path):
                os.makedirs(dan_obj_path)

            shutil.copytree(dan_obj_path, dan_before_path)




if os.path.isdir(W_jeon_path):
    W_jeon_list = os.listdir(W_jeon_path)
    W_jeon_list = sorted(W_jeon_list)
    
    for i, folder in enumerate(tqdm(W_jeon_list)):
        if folder.count('-') < 6:
            continue
        else :
            i = i+1
            jeon_before_path = os.path.join(W_jeon_path, folder, 'lidar', 'lidar_label')
            jeon_obj_path = os.path.join(U_jeon_path, folder, 'lidar', 'lidar_label')
                
            print('{}번째_전방향: {}'.format(i, jeon_before_path))
            print('{}번째_전방향: {}\n'.format(i, jeon_obj_path))
            
            if os.path.isdir(jeon_before_path):
                shutil.rmtree(jeon_before_path)

            if not os.path.isdir(jeon_obj_path):
                os.makedirs(jeon_obj_path)
                
            shutil.copytree(jeon_obj_path, jeon_before_path)

# In[ ]:




