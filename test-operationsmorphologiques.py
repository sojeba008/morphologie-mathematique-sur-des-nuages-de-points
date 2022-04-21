# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 16:59:52 2022

@author: Jean-baptiste
"""
import numpy as np
import OperationsMorphologiques
import Visualization as v
op = OperationsMorphologiques.OperationsMorphologique()
centre = [1,1,1]
el_struct = a_3d_array = np.zeros((3, 3, 3))
#el_struct[0][1][1]=1
#el_struct[1][1][1]=1
#el_struct[1][0][1]=1
#el_struct[1][2][1]=1
#el_struct[1][1][0]=1
#el_struct[1][1][2]=1
#el_struct[2][1][1]=1
el_struct[0][1][1]=1
el_struct[1][1][1]=1
el_struct[1][0][1]=0
el_struct[1][2][1]=0
el_struct[1][1][0]=1
el_struct[1][1][2]=0
el_struct[2][1][1]=1
print(el_struct)

v.visualize("data/chaiseFormated-H100-Moyenne-Empirique.txt")
#temp = op.erosion_binaire("data/open3d-Binaire.txt", el_struct, centre)


temp = op.dilatation("data/chaiseFormated-H100-Moyenne-Empirique.txt", el_struct, centre)
v.visualize(temp)


temp = op.ouverture_binaire("data/open3d-Binaire.txt", el_struct, centre)
v.visualize(temp)

temp = op.ouverture_binaire("data/open3d-Binaire-fermeture.txt", el_struct, centre)
v.visualize(temp)

el_struct=[[[0,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,1,1],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]
el_struct=[[[0,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,1,1],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]
#np.transpose(el_struct, axes=[0,1,2])


def getSymmetry(el_struct):
    i=0
    while i<len(el_struct):
        j=0
        while j<len(el_struct[0]):
            el_struct[i][j]=list(reversed(el_struct[i][j])) 
            j+=1
        i+=1
    el_struct= list(reversed(el_struct)) 
    return el_struct