# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 02:13:34 2022

@author: Jean-baptiste
"""
from time import sleep
import sys

import numpy as np
import pandas as pd
import Voxelization as v
class OperationsMorphologique:
    df = []
    df_copy = []
    df_length = 0
    def __init__(self):
        pass
    
    #def printProgressBar(self,value,label):
    #    n_bar = 40 #size of progress bar
    #    j= int(value)/100
    #    sys.stdout.write('\r')
    #    bar = '█' * int(n_bar * j)
    #    bar = bar + '-' * int(n_bar * (1-j))
    #
    #    sys.stdout.write(f"{label.ljust(10)} | [{bar:{n_bar}s}] {int(100 * j)}% ")
    #    sys.stdout.flush()
    
  


    def getNeighbors(self, tab):
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

    def erosion_binaire(self,filename="", el_struct=[], df=[], time=1, getDataframe=False, output="" ) :
        if len(df)==0 and type(df)==list:  
            df = pd.read_csv(filename, delimiter=" ", names=["i","j","k","r","g","b"])
        result = df.copy()
        df_length = len(df)
        neighbors = self.getNeighbors(el_struct)
        for ndf in range (len(df)):
            p=df.iloc[ndf]
            for n in range(len(neighbors[0])):
                 x=int(p['i'])
                 y=int(p['j'])
                 z=int(p['k'])
                 i,j,k= x+neighbors[0][n],y+neighbors[1][n],z+neighbors[2][n]
              
                 exist = df[(i==df['i'] ) &  (j==(df['j'])) &  (k==(df['k']))  ]
                 
                 if len(exist)==0:
                     result.drop(index=ndf,inplace=True)
                     break  
        if output=="": output = str(filename.split(".")[0])+"-erosionBinaire.txt"
        if getDataframe : 
            return result
        else:
            result[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
        return output
      
    

    
    def dilatation_binaire(self, filename="", el_struct=[],df=[] , time=1, getDataframe=False, output="" ) :
        if len(df)==0 and type(df)==list:  
            df = pd.read_csv(filename, delimiter=" ", names=["i","j","k","r","g","b"])
        result = df.copy()
        neighbors = self.getNeighbors(el_struct)
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
                     result = result.append(new_row, ignore_index=True)
                     
        if getDataframe : 
            return result
        else:
            result[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
        return output


    def ouverture_binaire(self, filename="", el_struct=[], df=[] ,getDataframe=False) :
        if len(df)==0 and type(df)==list:  
            df = pd.read_csv(filename, delimiter=" ", names=["i","j","k","r","g","b"])
        erode = self.erosion_binaire(df=df, el_struct=el_struct, getDataframe=True)
        dilate = self.dilatation_binaire(df=erode,el_struct=el_struct, getDataframe=True)
        output = str(filename.split(".")[0])+"-ouvertureBinaire.txt"
        
        if getDataframe : 
            return dilate
        else:
            dilate[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
        return output
    
    def fermeture_binaire(self, filename, el_struct, getDataframe="") :
        dilate = self.dilatation_binaire(filename, el_struct, getDataframe=True)
        erode = self.erosion_binaire(df=dilate,el_struct=el_struct, getDataframe=True)
        output = str(filename.split(".")[0])+"-fermetureBinaire.txt"
        if getDataframe : 
            return erode
        else:
            erode[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
        return output
    




    def getSymmetry(self, el_struct):
        i=0
        while i<len(el_struct):
            j=0
            el_struct[i]=list(reversed(el_struct[i]))
            while j<len(el_struct[0]):
                el_struct[i][j]=list(reversed(el_struct[i][j])) 
                j+=1
            i+=1
        el_struct= list(reversed(el_struct)) 
        return el_struct






    def morpho(self, df, el_struct, operation="erosion"):   
        result = df.copy()
        neighbors = self.getNeighbors(el_struct)
        for ndf in range (len(df)):
            r = []
            g = []
            b = []
            p = df.iloc[ndf]
            for n in range(len(neighbors[0])):
                 x=int(p['i'])
                 y=int(p['j'])
                 z=int(p['k'])
                 i,j,k=x+neighbors[0][n],y+neighbors[1][n],z+neighbors[2][n]
                 exist = df[(i==df['i'] ) &  (j==(df['j'])) &  (k==(df['k']))  ]
                    
                 if(len(exist)==1):
                        r.append(exist.iloc[0]['r'])
                        g.append(exist.iloc[0]['g'])
                        b.append(exist.iloc[0]['b']) 
                        
            if operation=="dilatation" and len(r)>0 :
                #print(r)
                #print(str(max(r))+" "+str(max(g))+" "+str(max(b)) )
                result['r'][ndf] = max(r)
                result['g'][ndf] = max(g)
                result['b'][ndf] = max(b)
            elif operation=="erosion" and len(r)>0 :
                #print(r)
                result['r'][ndf] = min(r)
                result['g'][ndf] = min(g)
                result['b'][ndf] = min(b)
        return result


    def erosion(self, filename="", el_struct=[], df=[], centre=[], getDataframe=False, output=""    ) :
        if len(df)==0 and type(df)==list:  
            df = pd.read_csv(filename, delimiter=" ", names=["i","j","k","r","g","b"])
        print(df)
        erode = self.morpho(df, el_struct, operation="erosion")
        if getDataframe : return erode
        if output=="": output = str(filename.split(".")[0])+"-erosion.txt";
        erode[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
        return output
    #
    
    def dilatation(self,filename="",el_struct=[], df=[], centre=[], getDataframe=False, output=""  ) :
        if len(df)==0 and type(df)==list:  
            df = pd.read_csv(filename, delimiter=" ", names=["i","j","k","r","g","b"])
        dilate = self.morpho(df, el_struct, operation="dilatation")
        
        if getDataframe : return dilate
        if output=="": output = str(filename.split(".")[0])+"-dilatation.txt";
        dilate[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
        return output
    #


    def ouverture(self, filename="", el_struct=[], df=[], centre=[],getDataframe=False, output="") :
        if len(df)==0 and type(df)==list: df = pd.read_csv(filename, delimiter=" ", names=["i","j","k","r","g","b"])
        erode = self.erosion(filename=filename, df=df,el_struct=el_struct, centre=centre, getDataframe=True)
        el_struct = self.getSymmetry(el_struct)
        ouverture = self.dilatation(df=erode, el_struct=el_struct, centre=centre,getDataframe=True)
        if getDataframe : return ouverture
        output = str(filename.split(".")[0])+"-ouverture.txt"
        ouverture[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
        return output
    
    def fermeture(self, filename="", el_struct=[], df=[], centre=[],getDataframe=False, output="") :
        if len(df)==0 and type(df)==list: df = pd.read_csv(filename, delimiter=" ", names=["i","j","k","r","g","b"])
        dilate = self.erosion(filename=filename,df=df,el_struct=el_struct, centre=centre, getDataframe=True)
        el_struct = self.getSymmetry(el_struct)
        fermeture = self.erosion(df=dilate, el_struct=el_struct, centre=centre,getDataframe=True)
        if getDataframe : return fermeture
        output = str(filename.split(".")[0])+"-fermeture.txt";
        fermeture[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
        return output
    
    
    
    def lantuejoulSkel(self, filename="", el_struct=[], df=[], getDataframe=False, output=""):
        if len(df)==0 and type(df)==list: df = pd.read_csv(filename, delimiter=" ", names=["i","j","k","r","g","b"])
        
        erode = self.erosion_binaire(df=df, el_struct=el_struct, getDataframe=True)
        it = 0
        skeleton = pd.DataFrame({'index':[], 'i': [], 'j': [], 'k': [], 'r': [], 'g': [], 'b': []})
        while (len(erode)>0):
            if it>0:
                erode = self.erosion_binaire(df=erode, el_struct=el_struct, getDataframe=True)
            erode = erode.reset_index(drop=True)
            ouverture_erode = self.ouverture_binaire(df=erode, el_struct=el_struct, getDataframe=True);
            
            try:
                newSkeletonVoxels = erode.drop(ouverture_erode.index)
            except Exception:
                pass
            skeleton = pd.concat([skeleton, newSkeletonVoxels ]).drop_duplicates(keep="first")
            it+=1
            print("Iteration : "+str(it)+" | Erode size "+str(len(erode)))
            #break
        if getDataframe : return skeleton
        output = str(filename.split(".")[0])+"-skeleton.txt";
        skeleton[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
        return output