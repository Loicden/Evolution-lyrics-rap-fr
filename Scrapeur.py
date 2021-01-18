import os
import csv
import requests
import itertools
import re
from collections import OrderedDict
from operator import itemgetter
import bs4
from bs4 import BeautifulSoup
"""
#%% Albums selon la page de l'artiste
requete = requests.get("https://genius.com/artists/Nepal")
page = requete.content
soup = BeautifulSoup(page, features="lxml")

Albums = []
for alb in soup.find_all('a', "vertical_album_card", href=True):
    date = alb.find('div', 'vertical_album_card-info')
    date = str(date.div.string)
    date = date.replace('\n', '')
    date = date.replace(' ', '')
    album = [alb['title'], date, alb['href']]
    Albums.append(album)

#%% Pistes selon l'album
for Album in Albums:
    print()
    print(Album[0])
    requete = requests.get(Album[2])
    page = requete.content
    soup = BeautifulSoup(page, features="lxml")
    
    Pistes = []
    for p in soup.find_all("a", "u-display_block", href=True):
        for string in p.h3.stripped_strings:
            if string != "Lyrics":
                if '(' in string :
                    ind = string.index('(')
                    nom = string[:ind-1]
                else :
                    nom = string
        piste = [nom, p['href']]
        print(piste)

#%% Paroles selon le titre
        requete = requests.get(piste[1])
        page = requete.content
        soup = BeautifulSoup(page, 'html.parser')
        section = soup.find("div", "lyrics")
        
        while type(section) is not bs4.element.Tag:
            requete = requests.get(piste[1])
            page = requete.content
            soup = BeautifulSoup(page, 'html.parser')
            section = soup.find("div", "lyrics")
        
        Lyrics = section.p
        for child in Lyrics.children:
            if child.name == 'annotatable-image':
                Lyrics = Lyrics.next_sibling
                while Lyrics.name != 'p':
                    Lyrics = Lyrics.next_sibling
                
        Paroles = []
        temp = 0
        ignore = False
        for string in Lyrics.descendants:
            if temp > 10 :
                break
            if string == "\n" or string =="," or string ==", ":
                pass
            elif type(string) is bs4.element.NavigableString:
                string = string.replace('\n', '')
                if string[0] == '[' and string[-1] == ']':
                    #print("IGNORED -", string, "- IGNORED")
                    pass
                elif string[0] == '[':
                    ignore = True
                    #print("IGNORE TRUE", string)
                elif ']' in string :
                    ignore = False
                    #print("IGNORE FALSE", string)
                elif ignore == True :
                    #print("IGNORED", string)
                    pass
                else:
                    print('\t',string)
                    Paroles.append(str(string))
                    piste.append(Paroles)
                    Album.append(piste)
                    temp +=1
"""

#%% Paroles selon le titre
Lien = "https://genius.com/Nepal-jugements-lyrics"
#Lien = "https://genius.com/8850558"
requete = requests.get(Lien)
page = requete.content
soup = BeautifulSoup(page, 'html.parser')
section = soup.find("div", "lyrics")

while type(section) is not bs4.element.Tag:
    requete = requests.get(Lien)
    page = requete.content
    soup = BeautifulSoup(page, 'html.parser')
    section = soup.find("div", "lyrics")

Lyrics = section.p
for child in Lyrics.children:
    if child.name == 'annotatable-image':
        Lyrics = Lyrics.next_sibling
        while Lyrics.name != 'p':
            Lyrics = Lyrics.next_sibling
            
Paroles = []
ignore = False
for string in Lyrics.descendants:
    if string == "\n" or string =="," or string ==", ":
        pass
    elif type(string) is bs4.element.NavigableString:
        string = string.replace('\n', '')
        if string[0] == '[' and string[-1] == ']':
            pass
        elif string[0] == '[':
            ignore = True
        elif ']' in string :
            ignore = False
        elif ignore == True :
            pass
        else:
            Paroles.append(str(string))
            
#%% Dictionnaires
Dic_contractions = {"f'nêtre": 'fenêtre'}
Dic_argot = {"gole-ri": "drôle", "cons'": 'conso'}
Dic_ignore = ['a', 'ai', 'au', 'avais', 'avec', 'ce', 'ces', 'ceux', "c'que",
              'dans', 'de', 'des', 'dit', 'du', 'en', 'est', 'et', 'faire', 'fais',
              'fait', 'font', 'ici', 'ils', 'irai', 'la', 'le', 'les', 
              'ma', 'mais', 'me', 'mes', 'mon', 'ne', 'nos', 'notre', 'on', 'ou', 'où',
              'pas', 'plus', "p't'être", "p't-être", 'que', 'qui',
              'sa', 'si', 'sur', 'suis', 'ton', 'tu', 'un', 'une', 'veux', 'vos', "y'a", 'à', 'ça']
Dic_remove = ["l'", "d'", "m'", "s'", "c'", "n'", "j'", "qu'", "t'"]

Nb_je = 0

#%% Mapper
MAP = []

for line in Paroles :
    line = line.strip()
    words = line.split()
    
    for word in words :
        word = word.replace(',', '')
        word = word.replace('’', "'")
        word = word.replace('(', "")
        word = word.replace(')', "")
        if word == "":
            break
        word = word.replace('œ', "oe")
        word = word.lower()
        
        if word in Dic_contractions :
            word = Dic_contractions[word]
        if word in Dic_argot :
            word = Dic_argot[word]
            
        nettoyage = True            
        while nettoyage :
            word_bef = word
            for abb in Dic_remove :
                if word[:len(abb)] == abb:
                    word = word[len(abb):]
                    if abb == "j'": 
                        Nb_je += 1
            if word == word_bef:
                nettoyage = False

        MAP.append('%s\t%s' % (word, 1))
        
current_word = None
current_count = 0
word = None

MAP.sort()

#%% Reducer
Reduce = {}
for line in MAP:
    line = line.strip()
    word, count = line.split('\t', 1)

    try:
        count = int(count)
    except ValueError:
        continue
    
    if current_word == word :
        current_count += count
    else:
        if current_word and current_word not in Dic_ignore:
            Reduce[current_word] = current_count
        current_count = count
        current_word = word

if current_word == word:
    Reduce[current_word] = current_count
    
#print(Reduce)
Reduce_ordered = OrderedDict(sorted(Reduce.items(), key = itemgetter(1), reverse = True))
for key, value in Reduce_ordered.items():
    print(key, '\t', value)
    pass
print()
if 'je' in Reduce :
    Nb_je += Reduce['je']
print('Nombre de "je" :', Nb_je)