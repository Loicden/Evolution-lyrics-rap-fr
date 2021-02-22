# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:34:57 2021

@author: Loïc
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 10:20:26 2021

@author: Loïc
"""
import os
import csv
import requests
import itertools
import re
import string
import pprint
import io
from collections import OrderedDict
from operator import itemgetter
import bs4
from bs4 import BeautifulSoup

#%% Album
Album_url = 'https://genius.com/albums/Disiz-la-peste/Le-poisson-rouge'
Album = []

#%% Pistes selon l'album
def get_lyrics(Album_url):
    print()
    requete = requests.get(Album_url)    # On prend l'URL
    page = requete.content
    soup = BeautifulSoup(page, features="lxml")
    
    Pistes = []     # Liste des pistes de l'album
    
    Titre = soup.find('h1', 'header_with_cover_art-primary_info-title header_with_cover_art-primary_info-title--white').string
    print(Titre)
    Artiste = soup.find('a', 'header_with_cover_art-primary_info-primary_artist').string
    print(Artiste)
    Date = soup.find('div', 'metadata_unit').string[-4:]
    print(Date)
    
    Album.append(Titre)
    Album.append(Artiste)
    Album.append(Date)
    Album.append(Album_url)
    
    for p in soup.find_all("a", "u-display_block", href=True):
        for string in p.h3.stripped_strings:
            if string != "Lyrics":  # On passe la première ligne "Lyrics"
                if '(' in string :  # On récupère le nom de la piste en retirant l'artiste en feat s'il y en a un
                    nom = string[:string.index('(')-1]
                else :
                    nom = string
        if ' by\xa0' in nom :
            nom = nom[:nom.index(' by\xa0')]
        piste = [nom.strip('\u200b'), p['href']]
        print('\t', piste[0])

#%% Paroles selon le titre
        requete = requests.get(piste[1]) # On récupère l'URL de la piste
        page = requete.content
        soup = BeautifulSoup(page, 'html.parser')
        
        Nfound = soup.find("div", "render_404") # Parfois, la page est référencée mais n'existe pas encore
        if Nfound != None:
            continue
        
        section = soup.find("div", "lyrics")
        
        while type(section) is not bs4.element.Tag: # Parfois le chargement ne fonctionne pas, on recommence tant que c'est le cas
            requete = requests.get(piste[1])
            page = requete.content
            soup = BeautifulSoup(page, 'html.parser')
            section = soup.find("div", "lyrics")
        
        Lyrics = section.p
        
        if Lyrics == None:  # Parfois on a une page sans lyrics
            continue
        
        for child in Lyrics.children:
            if child.name == 'annotatable-image':   # On évite la balise de pub
                Lyrics = Lyrics.next_sibling
                if type(Lyrics) is not bs4.element.Tag :
                    continue 
                while Lyrics.name != 'p':
                    Lyrics = Lyrics.next_sibling
                    
        if type(Lyrics) is not bs4.element.Tag : # Il n'y a pas de lyrics
            continue
        
        Paroles = []
        #temp = 0    # Clic d'arrêt pour les tests
        ignore = False  # Utile pour ne pas prendre les indications de noms de parties, ou d'artistes qui chante
        for string in Lyrics.descendants:
            #if temp > 1000 :
                #break
            if string == "\n" or string =="," or string ==", ":
                pass
            elif type(string) is bs4.element.NavigableString: # On évite la balise de lien vers un commentaire
                string = string.replace('\n', '')
                if string[0] == '[' and string[-1] == ']':
                    #print("IGNORED -", string, "- IGNORED")
                    pass
                elif string[0] == '[' and string[-2] == 'x':
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
                    #print('\t',string)
                    Paroles.append(str(string))
                    #temp +=1
                    
        print('\t' + '\t' + "Nombre de lignes :", len(Paroles))
        if Paroles != []:
            piste.append(Paroles)
            Album.append(piste)
        
#%% Scraping

pistes = get_lyrics(Album_url)

#%% Mapper
def mapper(Paroles) : # Entrée tableau des lignes
    Map = []
    # Je compte les nombres de "je" dans les textes, je pense que ça peut en dire long sur l'artiste :smiley_yeux:
    Nb_je = 0
    for line in Paroles :
        line = line.strip()     # On retire les espaces avant et après
        line = line.translate(str.maketrans('', '', Ponct)) # On retire la ponctuation
        #line = line.replace('-', ' ') # On remplace les tirets par des espaces
        words = line.split()    # On sépare les mots

        
        for word in words :
            word = word.replace('’', "'")
            word = word.replace('œ', "oe")
            if word == "":
                break               # Si la chaîne est vide, ça dégage
            word = word.lower()     # Tout en minuscule
            
            if word in Dict_contractions :
                word = Dict_contractions[word]
            if word in Dict_argot :
                word = Dict_argot[word]
                
            nettoyage = True    # Suppression des abbréviations en début de mot
            while nettoyage :
                word_bef = word
                for abb in Dict_remove :
                    if word[:len(abb)] == abb:
                        word = word[len(abb):]
                        if abb == "j'": 
                            Nb_je += 1
                if word == word_bef:    # Si aucune oppération n'a été effectuée sur le mot, on a fini
                    nettoyage = False

            if word == "":
                break               # Si la chaîne est vide, ça dégage
            Map.append('%s\t%s' % (word, 1))
            
    Map.sort()
    return Map, Nb_je

#%% Reducer
def reducer(Map):
    Reduce = {}    
    current_word = None
    current_count = 0
    word = None

    for line in Map :
        line = line.strip()
        #print(line)
        
        try:
            line[:1] != '\t'
        except ValueError:
            continue
        
        word, count = line.split('\t', 1)
    
        try:    
            count = int(count)  # On regarde si count est bien un nombre
        except ValueError:
            continue
        
        if current_word == word :
            current_count += count
        else:
            if current_word and current_word not in Dict_ignore: 
                Reduce[current_word] = current_count
            current_count = count
            current_word = word
    
    if current_word == word:
        Reduce[current_word] = current_count
        
    return Reduce
    
#%% Dictionnaires
Dict_contractions = {"f'nêtre": 'fenêtre'}
Dict_argot = {"gole-ri": "drôle", "cons'": 'conso'}
Dict_ignore = ['a', 'ai', 'au', 'avais', 'avec', 'ce', 'ces', 'ceux', "c'que",
              'dans', 'de', 'des', 'dit', 'du', 'en', 'est', 'es', 'et', 'faire', 'fais',
              'fait', 'font', 'ici', 'ils', 'irai', 'la', 'le', 'les', 
              'ma', 'mais', 'me', 'mes', 'mon', 'ne', 'nos', 'notre', 'on', 'ou', 'où',
              'pas', 'plus', "p't'être", "p't-être", 'que', 'qui',
              'sa', 'son', 'se', 'ses', 'sans', 'si', 'sont', 'sur', 'suis', 'ta',
              'te', 'tes', 'ton', 'tu', 'un', 'une', 'veux', 'vos', 'y', "y'a", 'à', 'ça', 
              'your', 'he', 'eh', 'étais', 'était', 'get', 'to', 'the', 'vais', 'ah', 
              'ha', 'no', 'ho', 'là', 'quoi', 'donc', 'viens', 'hey', 'sais', 'as', 'han', '-']
Dict_remove = ["l'", "d'", "m'", "s'", "c'", "n'", "j'", "qu'", "t'"]

#%% Mapping and reducing
Ponct = '!"#$%&\()*+,./:;<=>?@[\\]^_`{|}~—«»'

# On classe les mots sur tout l'album
print('#---------------------------#')
print(Album[:3])
print()
Reduce_album = {}
for i in Album[4:]:
    Map, Nb_je = mapper(i[-1])
    Reduce = reducer(Map)
    if Nb_je != 0:
        if 'je' in Reduce :
            Reduce['je'] += Nb_je
        else:
            Reduce['je'] = Nb_je
    i.append(Reduce)
    i.append(Nb_je)       
    total = sum(Reduce.values(), 0.0)
    Reduce = {k: v / total for k, v in Reduce.items()}
    
    if Reduce_album == {}:
        Reduce_album = Reduce
    else:
        Reduce_album = {k: Reduce_album.get(k, 0) + Reduce.get(k, 0) 
                        for k in set(Reduce_album) | set(Reduce)}

total = sum(Reduce_album.values(), 0.0)
Reduce_album = {k: v / total for k, v in Reduce_album.items()}

Reduce_ordered = OrderedDict(sorted(Reduce_album.items(), key = itemgetter(1), reverse = True))
temp = 0
for i in Reduce_ordered:
    print(i, '\t', Reduce_ordered[i])
    temp += 1
    if temp > 5: # Nb de mots qu'on veut afficher
        break
    
#%% Création du CSV
with io.open(Album[1] + '_' + Album[0].replace('/', '') + '_' + Album[2] + '.csv', 'w', encoding="utf-8") as f:
    for key in Reduce_ordered.keys():
        f.write("%s,%s\n"%(key,Reduce_ordered[key]))