# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 01:40:21 2022

@author: sojeb
"""

import numpy as np
import pandas as pd
import open3d as o3d

def visualize(filename="") :
    pcd = o3d.io.read_point_cloud(filename, format='xyzrgb')
    o3d.visualization.draw_geometries([pcd])
    
    
def visualizeFromDataFrame(df) :
    output="_temp/temp.txt";
    df[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
    pcd = o3d.io.read_point_cloud(output, format='xyzrgb')
    o3d.visualization.draw_geometries([pcd])