# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 16:59:52 2022

@author: Jean-baptiste
"""
import numpy as np
import OperationsMorphologiques
import Visualization as v
op = OperationsMorphologiques.OperationsMorphologique()

#v.visualize("data/chaiseFormated-H100-Moyenne-Empirique.txt")


el_struct = [[[0,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,1,1],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]
temp = op.ouverture("data/chaiseFormated-H100-Moyenne-Empirique.txt", el_struct, getDataframe=True)
temp1 = op.ouverture(df=temp, el_struct=el_struct, getDataframe=True)


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
el_struct = [[[0,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,1,1],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]
v.visualize("data/chaiseFormated-H100-Binaire.txt")
temp = op.erosion_binaire("data/chaiseFormated-H100-Binaire.txt", el_struct, getDataframe=True)
temp = op.dilatation_binaire("data/chaiseFormated-H100-Binaire.txt", el_struct, getDataframe=True)
temp = op.fermeture_binaire("data/chaiseFormated-H100-Binaire.txt", el_struct, getDataframe=True)



temp = op.erosion("data/chaiseFormated-H100-Moyenne-Empirique.txt", el_struct, getDataframe=True)




















temp = op.dilatation(filename="data/chaiseFormated-H100-Moyenne-Empirique.txt",el_struct=el_struct, centre=centre)
v.visualize(temp)

temp = op.erosion(filename="data/chaiseFormated-H100-Moyenne-Empirique.txt",el_struct=el_struct, centre=centre)
v.visualize(temp)

o1 = op.ouverture(filename="data/chaiseFormated-H100-Moyenne-Empirique.txt",el_struct=el_struct, centre=centre, getDataframe=True)
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
o2 = op.ouverture(df=o1.copy(),el_struct=el_struct, centre=centre,getDataframe=True)
#v.visualize(temp)


f1 = op.fermeture(filename="data/chaiseFormated-H100-Moyenne-Empirique.txt",el_struct=el_struct, centre=centre, getDataframe=True)
f2 = op.fermeture(df=o1.copy(),el_struct=el_struct, centre=centre,getDataframe=True)


temp = op.fermeture(filename="data/chaiseFormated-H100-Moyenne-Empirique.txt",el_struct=el_struct, centre=centre)
v.visualize(temp)






temp = op.ouverture_binaire("data/open3d-Binaire.txt", el_struct, centre)
v.visualize(temp)

temp = op.ouverture_binaire("data/open3d-Binaire-fermeture.txt", el_struct, centre)
v.visualize(temp)

el_struct=[[[0,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,1,1],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]
el_struct=[[[0,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,1,1],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]
el_struct=[[[1,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,1,1],[0,0,0]],[[0,1,0],[0,1,0],[0,0,0]]]
#np.transpose(el_struct, axes=[0,1,2])


def getSymmetry(el_struct):
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
el_struct = getSymmetry(el_struct)
print(el_struct)