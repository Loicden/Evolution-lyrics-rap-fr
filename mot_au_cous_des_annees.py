# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:42:14 2021

@author: maxim
"""
import os
import csv

Path = os.getcwd()



def fusion_annee(mot): 

        fichiers = [f for f in os.listdir(Path) if f.startswith("albums") and f.endswith(".csv")]
        if len(fichiers) == 0:
            return 
        
        
        dic = {}
                    
        for path in fichiers: 
            annee = path[7:11]

            with open(path, newline='', encoding='utf-8') as csvfile:
                linereader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in linereader:
                    word = row[0]
                    count = float(row[1])
                    if word == mot :
                        dic.update({annee : count})
                        break

                    
        with open(Path+"\\find_"+mot+".csv",  'w', newline='', encoding='utf-8') as csvfile:
            for key, value in dic.items():
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([key, value])

fusion_annee("je")