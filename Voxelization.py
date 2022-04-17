# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 23:10:12 2022

@author: jean-baptiste
"""


# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 23:52:50 2022

@author: ibram
"""
import numpy as np
import pandas as pd
import math
import open3d as o3d


def arrondi(value):
    return "{:.2f}".format(value)

def concat(arr1, arr2):
    for el in arr2:
        arr1.append(el)
    return arr1

def recor(df, voxels):
    line=df.iloc[0]
    i, j, k = int(line["vif"]), int(line["vjf"]), int(line["vkf"])    
    req = df[(i==df['vif'])  &  (j==df['vjf']) &  (k==df['vkf'])  ]

    to_remove = req.index.tolist()

    new_row = {"i":i, "j":j, "k":k, "points":req , "I":len(to_remove)}
    voxels=voxels.append(new_row, ignore_index=True)
  
    df.drop(index = to_remove, inplace=True)
    return df, voxels

def binariser(val):
    if val>0:
        return 0
    return 1

def moyenne_empirique(pts,c):
    somme = pts[c].sum()
    cardinalite = len(pts)
    return somme/cardinalite

def voxelize(filename="data/chaise.txt",h=100, algorithm=""):
    """
    Cette foncion permet de voxeliser un nuage de points (Format xyzIrgb).
    Elle retourne le(s) chemins de(s) fichiers issu(s) de la voxelization
    ...
    
    ----------
    
    filename : str
        le chemin du nuage de points
    h : float
        largeur d'un voxel
    algorithm : str
        Le(s) type(s) d'algorithme à utiliser.
        Valeurs possibles : "" | "binaire" | "densite" | "Moyenne-Empirique"
        Valeur par défaut : ""
    """
    #filename='chaise.txt
    result = {}
    df = pd.read_csv(filename, delimiter=" ", names=["x","y","z","r","g","b"])
    
    #pcd = o3d.io.read_point_cloud("chaise.txt", format='xyzrgb')
    #o3d.visualization.draw_geometries([pcd])
    
    df['i'] = df['x'].apply(lambda val:int(float(val)*1000))
    df['j'] = df['y'].apply(lambda val:int(float(val)*1000))
    df['k'] = df['z'].apply(lambda val:int(float(val)*1000))
    
    Xmin=df['i'].min()
    Ymin=df['j'].min()
    Zmin=df['k'].min()
    
    xa=abs(Xmin)
    ya=abs(Ymin)
    za=abs(Zmin)
    
    df['vi'] = df['i'].apply(lambda val:int((val+xa)))
    df['vj'] = df['j'].apply(lambda val:int((val+ya)))
    df['vk'] = df['k'].apply(lambda val:int((val+za)))
                             
    
    Xmax=df['vi'].max()
    Ymax=df['vj'].max()
    Zmax=df['vk'].max()
    
    nbpixelx=int(Xmax/h)
    if Xmax%h>0:
        nbpixelx=nbpixelx+1
        Xmax=nbpixelx*h
    
    nbpixely=int(Ymax/h)
    if Ymax%h>0:
        nbpixely=nbpixely+1
        Ymax=nbpixely*h
        
    nbpixelz=int(Zmax/h)
    if Zmax%h>0:
        nbpixelz=nbpixelz+1
        Zmax=nbpixelz*h
    
    df['vif'] = df['vi'].apply(lambda val:int(((val)/h)))
    df['vjf'] = df['vj'].apply(lambda val:int(((val)/h)))
    df['vkf'] = df['vk'].apply(lambda val:int(((val)/h)))
    
    dg=df
    
    voxels = pd.DataFrame({'i' : 0, 'j':0, 'k':0,'points':[],"I":0 })
    total = len(dg)    
    while  len(dg)>0:
        dg, voxels = recor(dg, voxels)   
        print(str(arrondi(100*(total-len(dg))/total)+"% \r"))
    max_intensity = voxels['I'].max()
    voxels=voxels[voxels["I"]>0]
    voxels['r'] = voxels['I'].apply(lambda r:arrondi(float(r)/max_intensity))
    voxels['g'] = voxels['I'].apply(lambda g:arrondi(float(g)/max_intensity))
    voxels['b'] = voxels['I'].apply(lambda b:arrondi(float(b)/max_intensity))
    
    
    if(algorithm=="" or algorithm=="densite"):
        output = filename.split(".")[0]+"-h"+str(h)+"-Densite.txt"
        result['densite'] = output
        voxels[['i','j','k','r','g','b']].to_csv(filename.split(".")[0]+"-h"+str(h)+"-Densite.txt", sep=" ", index=False ,index_label=False, header=False)
    
    #pcd = o3d.io.read_point_cloud(filename.split(".")[0]+"Formated-H"+str(h)+"-densite.txt", format='xyzrgb')
    #o3d.visualization.draw_geometries([pcd])
    

    if(algorithm=="" or algorithm=="binaire"):
        voxels['r'] = voxels['I'].apply(lambda r:binariser(float(r)))
        voxels['g'] = voxels['I'].apply(lambda g:binariser(float(g)))
        voxels['b'] = voxels['I'].apply(lambda b:binariser(float(b)))
        output=filename.split(".")[0]+"-h"+str(h)+"-Binaire.txt";
        result['binaire'] = output
        voxels[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
        #pcd = o3d.io.read_point_cloud(filename.split(".")[0]+"Formated-H"+str(h)+"-Binaire.txt", format='xyzrgb')
        #print (pcd)
        #o3d.visualization.draw_geometries([pcd])
    
    if(algorithm=="" or algorithm=="Moyenne-Empirique"):  
        voxels['r'] = voxels['points'].apply(lambda pts:moyenne_empirique(pts,'r'))
        voxels['g'] = voxels['points'].apply(lambda pts:moyenne_empirique(pts,'g'))
        voxels['b'] = voxels['points'].apply(lambda pts:moyenne_empirique(pts,'b'))
        output = filename.split(".")[0]+"-h"+str(h)+"-Moyenne-Empirique.txt"
        result['Moyenne-Empirique'] = output
        voxels[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
    
    #pcd = o3d.io.read_point_cloud(filename.split(".")[0]+"-h"+str(h)+"-Moyenne-Empirique.txt", format='xyzrgb')
    #print (pcd)
    #o3d.visualization.draw_geometries([pcd])
    #([pcd])
    
    return result
