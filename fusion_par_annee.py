# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:42:14 2021

@author: maxim
"""
import os
import csv

Path = os.getcwd()

annees = [1980+i for i in range(41)]

def fusion_annee(ANNEE): 

        fichiers = [f for f in os.listdir(Path) if f.endswith(str(ANNEE)+".csv")]
        if len(fichiers) == 0:
            return 
        
        
        dic = {}
                    
        for path in fichiers: 
            with open(path, newline='', encoding='utf-8') as csvfile:
                linereader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in linereader:
                    word = row[0]
                    count = int(row[1])
                    if word not in dic.keys():
                        dic.update({word : count})
                    else :
                        dic[word] += count
                    
        with open(Path+"\\albums_"+str(ANNEE)+".csv",  'w', newline='', encoding='utf-8') as csvfile:
            for key, value in dic.items():
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([key, value])

for annee in annees : 
    fusion_annee(annee)