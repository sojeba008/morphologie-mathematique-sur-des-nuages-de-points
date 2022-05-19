# -*- coding: utf-8 -*-
"""
Created on Wed May 11 23:54:14 2022

@author: sojeb
"""
import pandas as pd
import Voxelization as vxl
import Visualization as v
import OperationsMorphologiques


#mat = [[1,3,4,6,7],[3,4,6,8,6],[4,6,8,6,4],[6,7,7,5,2],[7,6,4,3,1]]
mat = [[1,3,4,6,7],[3,4,6,7,6],[4,6,8,7,4],[6,8,6,5,3],[7,6,4,2,1]]
image = pd.DataFrame({'index':[], 'i': [], 'j': [], 'k': [], 'r': [], 'g': [], 'b': []})
for i in range(0,len(mat)):
    for j in range(0,len(mat[0])):
        new_row = {"i":i, "j":j, "k":0, "r":mat[i][j] ,"g":mat[i][j],"b":mat[i][j]}
        image = image.append(new_row, ignore_index=True)
        
        
image = image.drop(labels=["index"], axis="columns")


op = OperationsMorphologiques.OperationsMorphologique()


el_struct = [[[0,0,0],
              [0,0,0],
              [0,0,0]],
             
             
             [[0,1,0],
              [0,1,1],
              [0,0,0]], 
             
             [[0,0,0],
              [0,0,0],
              [0,0,0]]]



ouverture1 = op.ouverture(df=image, el_struct=el_struct,getDataframe=True)
ouverture2 = op.ouverture(df=ouverture1, el_struct=el_struct,getDataframe=True)


erosion = op.erosion(df=image, el_struct=el_struct,getDataframe=True)

dilatation = op.dilatation(df=erosion, el_struct=op.getSymmetry(el_struct),getDataframe=True)