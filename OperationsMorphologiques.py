# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 02:13:34 2022

@author: Jean-baptiste
"""

import numpy as np
import pandas as pd

class OperationsMorphologique:
    df = []
    df_copy = []
    def erosion_binaire_f(self, line, array):   
        i, j, k = float(line["i"]), float(line["j"]), float(line["k"])
        b = True
        for el in array :
            temp = len(self.df[(self.df['i']==(i+float(el[0]))) & (self.df['j']==(j+float(el[1]))) & (self.df['k'] == (k+float(el[2]))) & (((self.df['r']>0) & (self.df['r']<1)) | ((self.df['g']>0) & (self.df['g']<1)) | ((self.df['b']>0) & (self.df['b']<1)))])
            #print(str(temp)+" \n")
            temp = (temp > 0)
            b = b & temp
        
        if b==False :
            line['r2'] = 1 
            line['g2'] = 1 
            line['b2'] = 1 
        else:
            line['r2'] = line['r'] 
            line['g2'] = line['g']
            line['b2'] = line['b']
        return line
    
    
    def erosion_binaire(self,df, el_struct, centre ) :
        c0=centre[0]
        c1=centre[1]
        c2=centre[2]
        array = []
        i=-1
        for e1 in el_struct:
            i+=1
            j=-1
            for e2 in e1:
                j+=1
                k=-1
                for e3 in e2:
                    k+=1
                    if e3==1 and [i,j,k]!=centre : 
                        array.append([c0-i,c1-j,c2-k])
    
        self.df = self.df.apply(lambda x : self.erosion_binaire_f(x, array), axis=1)
        self.df['r'] = self.df['r2']
        self.df['g'] = self.df['g2']
        self.df['b'] = self.df['b2']
        return df
    
    
    def dilatation_binaire_f(self, line, array): 
        #global df_copy
        i, j, k = float(line["i"]), float(line["j"]), float(line["k"])
        for el in array:
            temp = (self.df[(self.df['i']==(i+float(el[0]))) & (self.df['j']==(j+float(el[1]))) & (self.df['k'] == (k+float(el[2])))])
            if len(temp) == 1 :
                temp = self.df_copy[(self.df_copy['i']==(i+float(el[0]))) & (self.df_copy['j']==(j+float(el[1]))) & (self.df_copy['k'] == (k+float(el[2])))]
                temp.iloc[0]['r'] = 0
                temp.iloc[0]['g'] = 0
                temp.iloc[0]['b'] = 0
            else:
                new_row = { "i": (i+float(el[0])), "j": (j+float(el[1])), "k":(k+float(el[2])),"r":0, "g":0, "b":0}
                self.df_copy = self.df_copy.append(new_row, ignore_index=True)
        return line
    
    def dilatation_binaire(self, df, el_struct, centre ) :
        c0=centre[0]
        c1=centre[1]
        c2=centre[2]
        array = []
        df_copy = self.df.copy()
        i=-1
        for e1 in el_struct:
            i+=1
            j=-1
            for e2 in e1:
                j+=1
                k=-1
                for e3 in e2:
                    k+=1
                    if e3==1 and [i,j,k]!=centre : 
                        array.append([c0-i,c1-j,c2-k])  
        print(len(df_copy))
        self.df = self.df.apply(lambda x : self.dilatation_binaire_f(x, array), axis=1)
        print(len(df_copy))
        self.df=self.df_copy
        df[['i','j','k','r','g','b']].to_csv("open3dDatasetFormated-D2-binaire-erosion.txt", sep=" ", index=False ,index_label=False, header=False)


#centre = [1,1,1]
#dilatation_binaire(df, el_struct, centre ) 
#dilatation_binaire(df, el_struct, centre ) 
#dilatation_binaire(df, el_struct, centre ) 