# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:42:14 2021

@author: maxim
"""
import os
import csv
from collections import OrderedDict

Path = os.getcwd()

annees = [1980+i for i in range(41)]

def fusion_annee(ANNEE): 

        fichiers = [f for f in os.listdir(Path) if f.endswith(str(ANNEE)+".csv") and not f.startswith("albums")]
        Nbfichiers = len(fichiers)
        if  Nbfichiers == 0:
            return 
        
        
        dic = {}
                    
        for path in fichiers: 
            with open(path, newline='', encoding='utf-8') as csvfile:
                linereader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in linereader:
                    word = row[0]
                    count = float(row[1])
                    if word not in dic.keys():
                        dic.update({word : count/Nbfichiers})
                    else :
                        dic[word] += count/Nbfichiers
        dic = OrderedDict(sorted(dic.items(), key=lambda t: t[0]))
        sortedDict = OrderedDict(sorted(dic.items(), key=lambda t: t[1], reverse=True))
        
        with open(Path+"\\albums_"+str(ANNEE)+".csv", newline='', encoding='utf-8') as csvfile:
            r = csv.reader(csvfile)
            data = [line for line in r]
                    
        with open(Path+"\\albums_"+str(ANNEE)+".csv", 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Mot','Occurrence'])
            for key, value in sortedDict.items():
                    writer.writerow([key, value])

for annee in annees : 
    fusion_annee(annee)