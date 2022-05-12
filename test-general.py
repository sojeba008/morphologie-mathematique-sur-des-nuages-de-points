# -*- coding: utf-8 -*-
"""
Created on Fri May  6 12:15:36 2022

@author: sojeb
"""

import Voxelization as vxl
import Visualization as v
import OperationsMorphologiques


filename="data/chaise.txt"
#test = vxl.voxelize(filename=filename, h=100,algorithm="")
test={"binaire":"data/chaiseFormated-H50-Binaire.txt","densite":"data/chaiseFormated-H50-Densite.txt",
      "Moyenne-Empirique":"data/chaiseFormated-H100-Moyenne-Empirique.txt"}
v.visualize(filename)

v.visualize(test['binaire'])

v.visualize(test['densite'])

v.visualize(test['Moyenne-Empirique'])

op = OperationsMorphologiques.OperationsMorphologique()
el_struct = [[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,1,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]

erode = op.erosion_binaire(test['binaire'], el_struct, getDataframe=True)
v.visualizeFromDataFrame(erode)

dilate = op.dilatation_binaire(test['densite'], el_struct, getDataframe=True)
v.visualizeFromDataFrame(dilate)


ouverture = op.ouverture_binaire(test['binaire'], el_struct, getDataframe=True)
v.visualizeFromDataFrame(ouverture)

ouverture2 = op.ouverture_binaire(df=ouverture, el_struct=el_struct, getDataframe=True)
v.visualizeFromDataFrame(ouverture2)


skel = op.lantuejoulSkel(filename = test['binaire'], el_struct=el_struct, getDataframe=True )
v.visualizeFromDataFrame(skel)



erode = op.erosion(filename=test['Moyenne-Empirique'], el_struct=el_struct, getDataframe=True)
v.visualizeFromDataFrame(erode)

dilatation = op.dilatation(filename=test['Moyenne-Empirique'], el_struct=el_struct, getDataframe=True)
v.visualizeFromDataFrame(dilatation)

ouverture = op.ouverture(filename=test['Moyenne-Empirique'], el_struct=el_struct, getDataframe=True)
v.visualizeFromDataFrame(ouverture)

fermeture = op.fermeture(filename=test['Moyenne-Empirique'], el_struct=el_struct, getDataframe=True)

fermeture2 = op.fermeture(df=fermeture, el_struct=el_struct, getDataframe=True)

fermeture3 = op.fermeture(df=fermeture2, el_struct=el_struct, getDataframe=True)


fermeture4 = op.fermeture(df=fermeture3, el_struct=el_struct, getDataframe=True)


fermeture5 = op.fermeture(df=fermeture4, el_struct=el_struct, getDataframe=True)
v.visualizeFromDataFrame(fermeture5)

#Verif idempotence
#verif = fermeture4==fermeture3
#vfalse = verif[(verif['r']==False) | (verif['g']==False) | (verif['b']==False)]









