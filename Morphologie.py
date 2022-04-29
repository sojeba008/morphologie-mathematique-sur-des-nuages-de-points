#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 22:09:18 2022

@author: diarra
"""


import open3d as o3d
import numpy as np
import pandas as pd

def arrondi(value):
    return "{:.2f}".format(value)


filename='data/chaiseFormated-H100-Binaire.txt'
df = pd.read_csv('data/chaiseFormated-H100-Binaire.txt', names=["i","j","k","r","g","b"], delimiter=" ")

#pcd = o3d.io.read_point_cloud(filename, format='xyzrgb')
#o3d.visualization.draw_geometries([pcd])



def getNeighbors(tab):
    taille = len(tab)
    res=[[],[],[]]
    for h in range(taille):
        for l in range(taille):
            for c in range(taille):
                if tab[h][l][c]==1:
                    res[0].append(h-1)
                    res[1].append(l-1)
                    res[2].append(c-1)
                    
    return res

tab=[[[0,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,1,1],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]
neighbors=getNeighbors(tab)
def dilatationBinaire(df,res,neighbors):
    
   for ndf in range (len(df)):
       p=df.iloc[ndf]
       for n in range(len(neighbors[0])):
            x=int(p['i'])
            y=int(p['j'])
            z=int(p['k'])
            i,j,k=x+neighbors[0][n],y+neighbors[1][n],z+neighbors[2][n]
         
            exist = df[(i==df['i'] ) &  (j==(df['j'])) &  (k==(df['k']))  ]
         
            if len(exist)==0:      
                new_row = {"i":i, "j":j, "k":k, "r":0 ,"g":0,"b":0}
                res=res.append(new_row, ignore_index=True)
   return res

dilate = dilatationBinaire(df,df.copy(),neighbors)
#dilate[['i','j','k','r','g','b']].to_csv(filename.split(".")[0]+"DilatationBin.txt", sep=" ", index=False ,index_label=False, header=False)



def erosionBinaire(df,res,neighbors):
   for ndf in range (len(df)):
       p=df.iloc[ndf]
       for n in range(len(neighbors[0])):
            x=int(p['i'])
            y=int(p['j'])
            z=int(p['k'])
            i,j,k= x+neighbors[0][n],y+neighbors[1][n],z+neighbors[2][n]
         
            exist = df[(i==df['i'] ) &  (j==(df['j'])) &  (k==(df['k']))  ]
            
            if len(exist)==0:
              
                res.drop(index=ndf,inplace=True)
                break                                                    
   return res
erode=erosionBinaire(df,df.copy(),neighbors)
erode[['i','j','k','r','g','b']].to_csv(filename.split(".")[0]+"ErosionBin.txt", sep=" ", index=False ,index_label=False, header=False)


def ouvertureBinaire(df,res,neighbors):
   erode = erosionBinaire(df, res, neighbors)
   result = dilatationBinaire(erode, erode.copy(), neighbors)
   return result

ouverure_1 = ouvertureBinaire(df,df.copy(),neighbors)
ouverure_2 = ouvertureBinaire(ouverure_1, ouverure_1.copy(),neighbors)


def fermetureBinaire(df,res,neighbors):
   dilate = dilatationBinaire(df, res, neighbors)
   result = erosionBinaire(dilate, dilate.copy(), neighbors)
   return result

fermeture_1 = fermetureBinaire(df, df.copy(), neighbors)

fermeture_2 = fermetureBinaire(fermeture_1, fermeture_1.copy(), neighbors)
    





