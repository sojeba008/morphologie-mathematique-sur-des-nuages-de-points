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
    
    
    def recap(self, df) :
        total = len(df)
        count_one = (len(df[df["r"]==1]))
        print("1:"+str(count_one)+"\n")     
        print("0:"+str(total-count_one)+"\n")    
    
    def erosion_binaire_f(self, line, array):   
        i, j, k = float(line["i"]), float(line["j"]), float(line["k"])
        b = True
        for el in array :
            temp = len(self.df[(self.df['i']==(i+float(el[0]))) & (self.df['j']==(j+float(el[1]))) & (self.df['k'] == (k+float(el[2]))) & (self.df['r']==0)])
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
        print(str(v.arrondi(float(line.name)/self.df_length))+"/1")
        print("|\n")
        #self.printProgressBar((100*v.arrondi(float(line.name)/self.df_length)), "Progression")
        return line
    
    
    def erosion_binaire(self,filename, el_struct, centre, time=1, getDataframe=False, output="" ) :
        self.df = pd.read_csv(filename, delimiter=" ", names=["i","j","k","r","g","b"])
        self.df_length = len(self.df)
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
        t=0
        while t<time: 
            self.df = self.df.apply(lambda x : self.erosion_binaire_f(x, array), axis=1)
            self.df['r'] = self.df['r2']
            self.df['g'] = self.df['g2']
            self.df['b'] = self.df['b2']
            t+=1
        if output=="" : output = str(filename.split(".")[0])+"-erosion.txt";
        
        self.recap(self.df)
        
        if getDataframe : 
            return self.df
        else:
            self.df[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
        return output
    
    
    def dilatation_binaire_f(self, line, array, time=1 ): 
        #global df_copy
        i, j, k = float(line["i"]), float(line["j"]), float(line["k"])
        if line['r'] ==0 :
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
    
    def dilatation_binaire(self, filename, el_struct, centre, time=1, getDataframe=False, output="" ) :
        self.df = pd.read_csv(filename, delimiter=" ", names=["i","j","k","r","g","b"])
        c0=centre[0]
        c1=centre[1]
        c2=centre[2]
        array = []
        self.df_copy = self.df.copy()
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
        n=0
        while n<time:
            print(len(self.df_copy))
            self.df = self.df.apply(lambda x : self.dilatation_binaire_f(x, array), axis=1)
            print(len(self.df_copy))
            self.df=self.df_copy
            n+=1
        if output=="": output = str(filename.split(".")[0])+"-dilatation.txt"
        
        self.recap(self.df)
        if getDataframe : 
            return self.df
        else:
            self.df[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
        return output


    def ouverture_binaire(self, filename, el_struct, centre) :
        df = self.erosion_binaire(filename, el_struct, centre, getDataframe=(True))
        df[['i','j','k','r','g','b']].to_csv("data/temp.txt", sep=" ", index=False ,index_label=False, header=False)
        output = str(filename.split(".")[0])+"-ouverture.txt"
        return self.dilatation_binaire("data/temp.txt", el_struct, centre, output=output)
    
    def fermeture_binaire(self, filename, el_struct, centre) :
        df = self.dilatation_binaire(filename, el_struct, centre, getDataframe=(True))
        df[['i','j','k','r','g','b']].to_csv("data/temp.txt", sep=" ", index=False ,index_label=False, header=False)
        output = str(filename.split(".")[0])+"-fermeture.txt"
        return self.erosion_binaire("data/temp.txt", el_struct, centre, output=output)












    def morpho_f(self, line, array,df_copy, typ):   
        i, j, k = float(line["i"]), float(line["j"]), float(line["k"])
        r = []
        g = []
        b = []
        for el in array :
            temp = (df_copy[(df_copy['i']==(i+float(el[0]))) & (df_copy['j']==(j+float(el[1]))) & (df_copy['k'] == (k+float(el[2])))])
            if(line.name==0): print(temp)
            if(len(temp)==1):
                r.append(temp.iloc[0]['r'])
                g.append(temp.iloc[0]['g'])
                b.append(temp.iloc[0]['b'])
                print(r)
         
        if typ=="dilatation" and len(r)>0 :
            line['r'] = max(r)
            line['g'] = max(g)
            line['b'] = max(b)
        elif typ=="erosion" and len(r)>0 :
            line['r'] = min(r)
            line['g'] = min(g)
            line['b'] = min(b)
        return line


    def erosion(self, filename, el_struct, centre ) :
        df = pd.read_csv(filename, delimiter=" ", names=["i","j","k","r","g","b"])
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
                        array.append([i-c0,j-c1,k-c2])
        print(array)
        #return 0
        df_copy=df.copy()
        df = df.apply(lambda x : self.morpho_f(x, array, df_copy,'erosion'), axis=1)
        output = str(filename.split(".")[0])+"-erosion.txt";
        df[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
        return output
    #
    
    def dilatation(self,filename, el_struct, centre ) :
        df = pd.read_csv(filename, delimiter=" ", names=["i","j","k","r","g","b"])
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
                        array.append([i-c0,j-c1,k-c2])
        print(array)
        #return 0
        df_copy=df.copy()
        df = df.apply(lambda x : self.morpho_f(x, array, df_copy,'dilatation'), axis=1)
        output = str(filename.split(".")[0])+"-dilatation.txt";
        df[['i','j','k','r','g','b']].to_csv(output, sep=" ", index=False ,index_label=False, header=False)
        return output
    #
