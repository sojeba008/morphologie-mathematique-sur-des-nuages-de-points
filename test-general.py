# -*- coding: utf-8 -*-
"""
Created on Fri May  6 12:15:36 2022

@author: sojeb
"""

import Voxelization as vxl
import Visualization as v
import OperationsMorphologiques


filename="data/chaise.txt"
test={"binaire":"data/chaiseFormated-H50-Binaire.txt","densite":"data/chaiseFormated-H50-Densite.txt",
      "Moyenne-Empirique":"data/chaiseFormated-H50-Moyenne-Empirique.txt"}
#test = vxl.voxelize(filename=filename, h=100,algorithm="")  #A décommenter pour faire la voxelisation

v.visualize(filename)

v.visualize(test['binaire'])

v.visualize(test['densite'])

v.visualize(test['Moyenne-Empirique'])

op = OperationsMorphologiques.OperationsMorphologique()
el_struct=[[[0,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0,1,1],[0,0,0]],[[0,1,0],[0,1,0],[0,0,0]]]

erode = op.erosion_binaire(test['binaire'], el_struct, getDataframe=True)
v.visualizeFromDataFrame(erode)

dilate = op.dilatation_binaire(test['binaire'], el_struct, getDataframe=True)
v.visualizeFromDataFrame(dilate)


ouverture = op.ouverture_binaire(test['binaire'], el_struct, getDataframe=True)
v.visualizeFromDataFrame(ouverture)

fermeture = op.fermeture_binaire(df=ouverture, el_struct=el_struct, getDataframe=True)
v.visualizeFromDataFrame(ouverture2)

el_struct= [[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,1,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]
skel = op.lantuejoulSkel(filename = test['binaire'], el_struct=el_struct, getDataframe=True )
v.visualizeFromDataFrame(skel)


el_struct= [[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,1,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]
erode = op.erosion(filename=test['Moyenne-Empirique'], el_struct=el_struct, getDataframe=True)
v.visualizeFromDataFrame(erode)

el_struct= [[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,1,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]
dilatation = op.dilatation(filename=test['Moyenne-Empirique'], el_struct=el_struct, getDataframe=True)
v.visualizeFromDataFrame(dilatation)

el_struct= [[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,1,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]
ouverture = op.ouverture(filename=test['Moyenne-Empirique'], el_struct=el_struct, getDataframe=True)
v.visualizeFromDataFrame(ouverture)

el_struct= [[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,1,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]
fermeture = op.fermeture(filename=test['Moyenne-Empirique'], el_struct=el_struct, getDataframe=True)
v.visualizeFromDataFrame(fermeture)

el_struct= [[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,1,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]
fermeture2 = op.fermeture(df=fermeture, el_struct=el_struct, getDataframe=True)

el_struct= [[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,1,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]
fermeture3 = op.fermeture(df=fermeture2, el_struct=el_struct, getDataframe=True)

el_struct= [[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,1,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]
fermeture4 = op.fermeture(df=fermeture3, el_struct=el_struct, getDataframe=True)

fermeture5 = op.fermeture(df=fermeture4, el_struct=el_struct, getDataframe=True)
v.visualizeFromDataFrame(fermeture5)

#Verif idempotence
#verif = (fermeture4==fermeture3)
#vfalse = verif[(verif['r']==False) | (verif['g']==False) | (verif['b']==False)]
#si la taille de vfalse est de 0 alors y'a pas de divergence entre les voxels. Donc idempotence.






#5 dilatations binaires + 5 erosions binaires
dilate = op.dilatation_binaire(test['binaire'], el_struct=el_struct, getDataframe=True)
dilate = op.dilatation_binaire(df=dilate, el_struct=el_struct, getDataframe=True)
#dilate = op.dilatation_binaire(df=dilate, el_struct=el_struct, getDataframe=True)
#dilate = op.dilatation_binaire(df=dilate, el_struct=el_struct, getDataframe=True)
#dilate = op.dilatation_binaire(df=dilate, el_struct=el_struct, getDataframe=True)


erode = op.erosion_binaire(df=dilate.reset_index(drop=True), el_struct=el_struct, getDataframe=True)
erode = op.erosion_binaire(df=erode.reset_index(drop=True), el_struct=el_struct, getDataframe=True)
#erosion_ = op.erosion_binaire(df=dilate, el_struct=el_struct, getDataframe=True)
#erosion_ = op.erosion_binaire(df=dilate, el_struct=el_struct, getDataframe=True)
#erosion_ = op.erosion_binaire(df=dilate, el_struct=el_struct, getDataframe=True)
v.visualizeFromDataFrame(erode)



#5 erosion binaires + 5 dilatation binaires
erode = op.erosion_binaire(test['binaire'], el_struct=el_struct, getDataframe=True)
erode = op.erosion_binaire(df=erode.reset_index(drop=True), el_struct=el_struct, getDataframe=True)

#dilate = op.dilatation_binaire(df=dilate, el_struct=el_struct, getDataframe=True)
#dilate = op.dilatation_binaire(df=dilate, el_struct=el_struct, getDataframe=True)
#dilate = op.dilatation_binaire(df=dilate, el_struct=el_struct, getDataframe=True)


dilate = op.dilatation_binaire(erode.reset_index(drop=True), el_struct=el_struct, getDataframe=True)
dilate = op.dilatation_binaire(df=dilate.reset_index(drop=True), el_struct=el_struct, getDataframe=True)
#erosion_ = op.erosion_binaire(df=dilate, el_struct=el_struct, getDataframe=True)
#erosion_ = op.erosion_binaire(df=dilate, el_struct=el_struct, getDataframe=True)
#erosion_ = op.erosion_binaire(df=dilate, el_struct=el_struct, getDataframe=True)
v.visualizeFromDataFrame(dilate)




