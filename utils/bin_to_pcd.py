# https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/utils/data_classes.py#L249

import pandas as pd
import numpy as np
import os
import sys
from tqdm import tqdm
import shutil
import open3d as o3d
import struct

ex_folder = "C:\\Users\\wq_ysw\\Desktop\\Lidar\\07 ex_folder"
bin_file = "C:\\Users\\wq_ysw\\Desktop\\Lidar\\07 ex_folder\\dan\\2020-11-25-06-51-04-01\\lidar\\lidar\\000000.bin"

pcdFileName = "C:\\Users\\wq_ysw\\Desktop\\Lidar\\000000.pcd"

def bin_to_pcd(binFileName):
    size_float = 4
    list_pcd = []

    with open(binFileName, "rb") as f:
        byte = f.read(size_float * 4)
        while byte:
            x, y, z, intensity = struct.unpack("ffff", byte)
            # list_pcd.append([x, y, z, intensity])
            list_pcd.append([x, y, z])
            byte = f.read(size_float * 4)

    np_pcd = np.asarray(list_pcd)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(np_pcd)
    return pcd

def read_bin_file(bin_file):
    pcd = bin_to_pcd(bin_file)
    # print(pcd_file)
    o3d.io.write_point_cloud(pcdFileName, pcd)


read_bin_file(bin_file)
pcd = o3d.io.read_point_cloud("C:\\Users\\wq_ysw\\Desktop\\Lidar\\000000.pcd") # Read the point cloud

print(pcd.points)
# o3d.visualization.draw_geometries([pcd]) # Visualize the point cloud 
