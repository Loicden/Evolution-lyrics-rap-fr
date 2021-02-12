# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:42:14 2021

@author: maxim
"""
import os
import csv
from collections import OrderedDict

Path = os.getcwd()

dic = {}

filin = open(Path+"/champs lexicaux.txt", 'r', encoding='utf-8')
lignes = filin.readlines()
for ligne in lignes:
    if len(ligne) != 1 :
        row = ligne.strip().split(" = ")
        champ = '"' + row[0] + '"'
        L = row[1].strip('][').split(', ')

        dic.update({champ : L})
    
   
with open(Path+"\\champs_guillemets"+".txt", 'w', newline='', encoding='utf-8') as filout:
        for key, value in dic.items():
                filout.write(key + " : " +  str(value) + ", ")
