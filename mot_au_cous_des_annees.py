# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:42:14 2021

@author: maxim
"""
import os
import csv
from collections import OrderedDict

Path = os.getcwd()



def fusion_annee(): 

        fichiers = [f for f in os.listdir(Path) if f.startswith("champs") and f[7:15] != "restants" and f.endswith(".csv")]
        if len(fichiers) == 0:
            return 
        
                    
        for path in fichiers: 
            annee = path[-8:-4]
            artiste = path[7:-9]
            dic = {}

            with open(path, newline='', encoding='utf-8') as csvfile:
                linereader = csv.reader(csvfile, delimiter=',', quotechar='|')
                champ_en_cours = "**"
                champ_count = 0
                Nbmots = 0
                for row in linereader:
                    word = row[0]
                    count = float(row[1])
                    champ = row[2]
                    if champ == champ_en_cours and Nbmots<=10:
                        champ_count += count 
                        Nbmots += 1 
                    else : 
                        dic.update({champ_en_cours : champ_count})
                        champ_en_cours = champ
                        champ_count = count
                        Nbmots = 0 

            dic = OrderedDict(sorted(dic.items(), key=lambda t: t[1], reverse=True))                
            with open(Path+"\\fusion_champ_"+artiste+"_"+annee+".csv",  'w', newline='', encoding='utf-8') as csvfile:
                for key, value in dic.items():
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([key, value])

fusion_annee()