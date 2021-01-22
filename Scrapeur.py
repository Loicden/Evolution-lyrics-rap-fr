import os
import csv
import requests
import itertools
import re
import string
import pprint
from collections import OrderedDict
from operator import itemgetter
import bs4
from bs4 import BeautifulSoup

#%% Nom de l'artiste
Artiste = '47ter' #Attention à l'entrer comme il est écrit dans l'URL de sa page genius

#%% Albums selon la page de l'artiste
def get_albums(Artiste):
    requete = requests.get("https://genius.com/artists/" + Artiste)
    page = requete.content
    soup = BeautifulSoup(page, features="lxml")
    
    Albums = []     # Liste des albums de l'artiste
    for alb in soup.find_all('a', "vertical_album_card", href=True):
        date = alb.find('div', 'vertical_album_card-info')
        if type(date.div) is not bs4.element.Tag :
            continue
        date = str(date.div.string)
        date = date.replace('\n', '')
        date = date.replace(' ', '')
        
        album = [alb['title'], Artiste, date, alb['href']] # Format [Titre, Auteur, Date, URL]
        Albums.append(album)
    return Albums

#%% Pistes selon l'album
def get_lyrics(Album):
    print()
    print(Album[0])
    print()
    requete = requests.get(Album[3])    # On prend l'URL
    page = requete.content
    soup = BeautifulSoup(page, features="lxml")
    
    Pistes = []     # Liste des pistes de l'album
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
                while Lyrics.name != 'p':
                    Lyrics = Lyrics.next_sibling
        
        Paroles = []
        temp = 0    # Clic d'arrêt pour les tests
        ignore = False  # Utile pour ne pas prendre les indications de noms de parties, ou d'artistes qui chante
        for string in Lyrics.descendants:
            if temp > 1000 :
                break
            if string == "\n" or string =="," or string ==", ":
                pass
            elif type(string) is bs4.element.NavigableString: # On évite la balise de lien vers un commentaire
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
                    #print('\t',string)
                    Paroles.append(str(string))
                    temp +=1
                    
        print('\t' + '\t' + "Nombre de lignes :", len(Paroles))
        piste.append(Paroles)
        Album.append(piste)
        
#%% Scraping

Albums = get_albums(Artiste)
for i in Albums :
    print(i)
print()
print("#---------------------------#")
for i in Albums :
    get_lyrics(i)

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
              'dans', 'de', 'des', 'dit', 'du', 'en', 'est', 'et', 'faire', 'fais',
              'fait', 'font', 'ici', 'ils', 'irai', 'la', 'les', 
              'ma', 'mais', 'me', 'mes', 'mon', 'ne', 'nos', 'notre', 'on', 'ou', 'où',
              'pas', 'plus', "p't'être", "p't-être", 'que', 'qui',
              'sa', 'sans', 'si', 'sont', 'sur', 'suis', 'ta', 'ton', 'tu', 'un', 'une', 'veux', 'vos', "y'a", 'à', 'ça']
Dict_remove = ["l'", "d'", "m'", "s'", "c'", "n'", "j'", "qu'", "t'"]

#%% Mapping and reducing
Ponct = '!"#$%&\()*+,./:;<=>?@[\\]^_`{|}~—«»'

# On classe les mots sur tout l'album [0]
for Album in Albums:
    Lyrics_album = []
    for i in Album:
        Lyrics_album += i[-1]
    Map, Nb_je = mapper(Lyrics_album)
    Reduce = reducer(Map)
    if Nb_je != 0:
        if 'je' in Reduce :
            Reduce['je'] += Nb_je
        else:
            Reduce['je'] = Nb_je
    print()
    print('#---------------------------#')
    print()
    Reduce_ordered = OrderedDict(sorted(Reduce.items(), key = itemgetter(1), reverse = True))
    temp = 0
    for i in Reduce_ordered:
        print(i, '\t', Reduce_ordered[i])
        temp += 1
        if temp > 10:
            break