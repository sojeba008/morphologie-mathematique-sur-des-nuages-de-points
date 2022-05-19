# -*- coding: utf-8 -*-
"""
Created on Thu May 19 14:41:11 2022

@author: sojeb
"""

filename="data/chaise.txt"
test={"binaire":"data/chaiseFormated-H30-Binaire.txt","densite":"data/chaiseFormated-H50-Densite.txt",
      "Moyenne-Empirique":"data/chaiseFormated-H50-Moyenne-Empirique.txt"}

import Voxelization as vxl
import Visualization as v
import OperationsMorphologiques

v.visualize(filename)
v.visualize(test['binaire'])
v.visualize(test['densite'])
v.visualize(test['Moyenne-Empirique'])

el_struct= [[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,1,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]]
op = OperationsMorphologiques.OperationsMorphologique()
# Image binaire
erode_binaire = op.erosion_binaire(test['binaire'], el_struct)
dilate_binaire = op.dilatation_binaire(test['binaire'], el_struct)
ouverture_binaire = op.ouverture_binaire(test['binaire'], el_struct)
fermeture_binaire = op.fermeture_binaire(test['binaire'], el_struct)

# Image fonction
erode = op.erosion(test['Moyenne-Empirique'], el_struct)
dilate = op.dilatation(test['Moyenne-Empirique'], el_struct)
ouverture = op.ouverture(test['Moyenne-Empirique'], el_struct)
fermeture = op.fermeture(test['Moyenne-Empirique'], el_struct)

# Squelette
squelette = op.lantuejoulSkel(filename = test['binaire'], el_struct=el_struct)





v.visualize(filename)
v.visualize(test['binaire'])
v.visualize(test['densite'])
v.visualize(test['Moyenne-Empirique'])

v.visualize("data/chaiseFormated-H50-Binaire-dilatationBinaire.txt")

v.visualize("data/chaiseFormated-H50-Binaire-erosionBinaire.txt")

v.visualize("data/chaiseFormated-H50-Binaire-ouvertureBinaire.txt")

v.visualize("data/chaiseFormated-H50-Binaire-fermetureBinaire.txt")

v.visualize("data/chaiseFormated-H50-Moyenne-Empirique-dilatation.txt")

v.visualize("data/chaiseFormated-H50-Moyenne-Empirique-erosion.txt")

v.visualize("data/chaiseFormated-H50-Moyenne-Empirique-ouverture.txt")

v.visualize("data/chaiseFormated-H50-Moyenne-Empirique-fermeture.txt")

v.visualize("data/chaiseFormated-H50-Binaire-skeleton.txt")


