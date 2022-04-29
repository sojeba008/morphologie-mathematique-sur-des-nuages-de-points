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
#df = pd.read_csv("open3dDatasetFormated-D2-Binaire.txt", names=["i","j","k","r","g","b"], delimiter=" ")
#df = df.head(10)
pcd = o3d.io.read_point_cloud(filename, format='xyzrgb')
#o3d.visualization.draw_geometries([pcd])
resdilater = df.copy()

reseroder=df.copy()

def element (tab,taille):
    res=[[],[],[]]
    for h in range(taille):
        for l in range(taille):
            for c in range(taille):
                if tab[h][l][c]==1:
                    res[0].append(h-1)
                    res[1].append(l-1)
                    res[2].append(c-1)
                    
    return res
    
#tab=[[[1,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,1,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]
tab=[[[0,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,1,1],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]
pos=element(tab, 3)


def correspondant(x,y,z,i,j,k):
    
    
    xr=i+x
    yr=j+y;
    zr=k+z;
    
    return xr,yr,zr
 
    
resdilater = df.copy()

reseroder=df.copy()

resouvert=df.copy()


resfermer=df.copy()
def dilatationbin(df,res,pos):
    
   for ndf in range (len(df)):
       p=df.iloc[ndf]
        
       for n in range(len(pos[0])):
                       x=int(p['i'])
                       y=int(p['j'])
                       z=int(p['k'])
                       i,j,k=correspondant(pos[0][n],pos[1][n],pos[2][n],x,y,z)
                    
                       exist = df[(i==df['i'] ) &  (j==(df['j'])) &  (k==(df['k']))  ]
                    
                       if len(exist)==0:      
                           new_row = {"i":i, "j":j, "k":k, "r":0 ,"g":0,"b":0}
                           res=res.append(new_row, ignore_index=True)
   return res
                    
                   
resdilater=dilatationbin(df,resdilater,pos)
    
resdilater[['i','j','k','r','g','b']].to_csv(filename.split(".")[0]+"DilatationBin.txt", sep=" ", index=False ,index_label=False, header=False)

pcd = o3d.io.read_point_cloud(filename.split(".")[0]+"DilatationBin.txt", format='xyzrgb')

o3d.visualization.draw_geometries([pcd])

def erosionbin(df,res,pos):
    
   for ndf in range (len(df)):
       p=df.iloc[ndf]
      
       for n in range(len(pos[0])):
                       x=int(p['i'])
                       y=int(p['j'])
                       z=int(p['k'])
                       i,j,k=correspondant(pos[0][n],pos[1][n],pos[2][n],x,y,z)
                    
                       exist = df[(i==df['i'] ) &  (j==(df['j'])) &  (k==(df['k']))  ]
                       
                       if len(exist)==0:
                           print(len(exist))
                           res.drop(index=ndf,inplace=True)
                           break
                       
                                                     
   return res
reseroder=erosionbin(df,reseroder,pos)
    
reseroder[['i','j','k','r','g','b']].to_csv(filename.split(".")[0]+"ErosionBin.txt", sep=" ", index=False ,index_label=False, header=False)

pcd = o3d.io.read_point_cloud(filename.split(".")[0]+"ErosionBin.txt", format='xyzrgb')

o3d.visualization.draw_geometries([pcd])


def ouverture(df,res,pos):
   
   reseroder=erosionbin(df,res,pos)
    
   reerod2=reseroder.copy()
   res=dilatationbin(reseroder,reerod2,pos )

   return res

resouvert=ouverture(df,resouvert,pos)

resouvert=ouverture(resouvert.copy(),resouvert,pos)


resouvert[['i','j','k','r','g','b']].to_csv(filename.split(".")[0]+"OuvertureBin.txt", sep=" ", index=False ,index_label=False, header=False)

pcd = o3d.io.read_point_cloud(filename.split(".")[0]+"OuvertureBin.txt", format='xyzrgb')

o3d.visualization.draw_geometries([pcd])


def fermeture(df,res,pos):
   
   resdilater=dilatationbin(df,res,pos)
    
   redilat2=resdilater.copy()
   res=erosionbin(resdilater,redilat2,pos )

   return res

resfermer=fermeture(df,resfermer,pos)
    
resfermer=fermeture(resfermer.copy(),resfermer,pos)
    
resfermer[['i','j','k','r','g','b']].to_csv(filename.split(".")[0]+"FermetureBin.txt", sep=" ", index=False ,index_label=False, header=False)

pcd = o3d.io.read_point_cloud(filename.split(".")[0]+"FermetureBin.txt", format='xyzrgb')

o3d.visualization.draw_geometries([pcd])








