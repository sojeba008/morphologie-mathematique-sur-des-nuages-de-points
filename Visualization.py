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