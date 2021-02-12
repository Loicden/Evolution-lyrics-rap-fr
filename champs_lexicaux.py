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

champs_lexicaux = {"argent" : ['gent-ar', 'euros', 'dollars', 'billets', 'portefeuille', 'money', 'monnaie', 'banque', 'banques', 'casino', 'sous', 'fric', 'blé', 'flouze', 'oseille', 'cash', 'pognon', 'pièces', 'thune', 'pèze', 'maille', 'moula', 'mula', 'moulaga', 'lovés', 'wari', 'biff', 'payer', 'paye', 'revendu'], "violence" : ['coup', 'coups', 'cogne', 'meurt', 'meurs', 'mourir', 'mort', 'die', 'tuerais', 'crève', 'cimetière', 'balles', 'armé', 'peur', 'guerre', 'crime', 'tombé', 'gang', 'clan', 'rivaliser', 'venger', 'vengeance', 'couteau', 'couteaux', 'fanatiques', 'coupe', 'létale', 'sirène', 'assassin', 'corrompt', 'danger', 'dangereuse', 'enfer', 'nazis', 'violent', 'pleurer', 'battre', 'fight', 'victimes', 'flingue', 'flingues', 'brûler', 'mafia', 'feu', 'fumée', 'menottes', 'blesser', 'cadavres', 'sang', 'saigner', 'viol', 'bagarrer', 'blessures', 'disloqué', 'cris', 'prison', 'revolvers', 'fusil', 'barrières', 'camo', 'caméra', 'casseurs', 'headshot', 'torture', 'bute'], "personnes" : ['homme', 'hommes', 'criminel', 'gangster', 'ennemi', 'ennemis', 'enemy', 'thug', 'coupable', 'voyous', 'bandit', 'gars', 'traîtres', 'guerrier', 'mec', 'mecs', 'gagnant', 'boy', 'aventurier', 'gava', 'gavas', 'reuf'], "musique" : ['rap', 'mélodie', 'paroles', 'album', 'musique', 'music', 'son', 'rappeur', 'mots', 'chansons', 'chante', 'couplet', 'disques', 'rime', 'dj', 'airs', 'concerts', 'club', 'voix', 'instru', 'vinyle'], "musique_termes_spécifiques" : ['92i', 'izi', 'kalash', 'boulbi', 'django'], "concepts_abstraits" : ['paix', 'question', 'questions', 'vérité', 'life', 'vie', 'vivre', 'futur', 'future', 'avenir', 'destin', 'monde', 'loi', 'âme', 'temps', 'années', 'chance', 'libre', 'rêve', 'esprit', 'conscience', 'sens', 'société'], "religieux" : ['mollah', 'jésus', 'halal', 'hallal', 'ciel', 'allah', 'dieu', 'enfer', 'paradis', 'démon', 'démons', 'diable', 'prophète', 'anges', 'priez'], "onomatopés" : ['wesh', 'ouais', 'yeah', 'hey', 'nan', 'no', 'oh', 'yo', 'ok', 'okay', 'eh', 'ah', 'ouaaais', 'uh', 'bah', 'youh', 'allo'], "ego" : ['swag', 'maître', 'leader', 'pèse', 'masta', 'boss', 'as', 'magiciens', 'beau', 'beaux', 'invincible', 'talent', 'génie', 'gifted'], "lieux" : ['street', 'city', 'terre', 'bled', 'rue', 'ville', 'métro', 'hôtel', 'boîte', 'maison', 'parc', 'parcs', 'marseille', 'afrique', 'paris', 'paname', 'français', 'afghanistan'], "noir" : ['black', 'renoi', 'nigga', 'niggas', 'niggiz', 'négro', 'négros', 'noir', 'noires'], "travail" : ['boulot', 'taf', 'taffé', 'biz', 'job', 'business', 'collègues', 'patrons', 'bureau', 'buildings'], "police" : ['flic', 'flics', 'keuf', 'cop'], "drogues" : ["toxico'", 'toxicoman', 'drogue', 'seringue', 'addict', 'cannabis', 'fonce-dé', 'high', 'grammes', 'fumé', 'joint', 'beuh', 'herbe', 'clope', 'cocaïne-lord'], "alcool" : ['alcool', 'bière', 'bistrot', 'alcoolique', 'bouteille', 'gin', 'vin', 'whisky', 'défoncé', 'boire', 'bois', 'cocktails', 'cocktail', 'canettes', 'scotch', 'bourrés', 'rre-ve', 'rres-ve'], "luxe" : ['maybach', 'diamants', 'millionnaire', 'or', 'luxe', 'palace'], "aime" : ['bien', 'pote', 'potes', 'poto', 'aime', 'mieux', 'préféré', 'coeur', 'belle', 'love', 'amour', 'amis', 'amitié', 'préfère', 'aimait', 'aimerais', 'love', 'loveur', 'sourire', 'souris', 'ensemble'], "émotions/adjectifs_positif" : ['force', 'puissance', 'fier', 'honnête', 'respect', 'calme', 'zen', 'confiance', 'mérite'], "émotions/adjectifs_négatif" : ['nerfs', 'soucis', 'crise', 'erreurs', 'souffert', 'souffrir', 'souffrance', 'triste', 'regrets', 'pire', 'stress', 'mal', 'larmes', 'peur', 'haine', 'marre', 'chagrin', 'mépris', 'seum', 'colère', 'envie', 'manque', 'rage', 'déshonneur', 'folie', 'fou', 'fous', 'sale', 'seul', 'personne', 'grosse', 'grave', 'faibles', 'faible', 'foutu', 'frustré', 'honte', 'énervé', 'errer', 'traîner', 'faute', 'feeling', 'dégoûté', 'douter', 'ennuis'], "exagération" : ['toujours', 'rien', 'jamais', 'tellement', 'tous', 'trop', 'vraiment', 'aucun'], "**" : ['fuck', 'putes', 'baise', 'baiser', 'couilles', 'nique', 'bâtard', 'gros', 'gueule', 'merde', 'shit', 'chatte', 'cul', 'foutre', '', 'merde', 'putain', 'twerke', 'embrouilles', 'chier', 'enfoiré', 'enculé', 'connard', 'salope', 'pétasses', 'bastard', 'conneries', 'bitches'], "je" : ['je', 'moi', 'oim', 'my'], "famille" : ['famille', "mif'", 'mama', 'maman', 'mère', 'mères', 'frère', 'frères', 'fils', 'grand-mère', 'grand-père', 'grands-parents', 'famille', 'daronne', 'garçon', 'pères', 'papa', 'enfant', 'enfants', 'mômes', 'gamins', 'soeur', 'cousin', "couz'", 'fillette'], "verlan" : ['rebeu', 'veau-cer', 'tur-fu', 'té-cô', 'trix-ma', 'seille-mar', 'screts-di', 'ients-cli', 'gol-mon', 'gent-ar', 'deur-vi', 'del-bor', 'cé-per', 'che-blan', 'ieux-sér', 'àl', 'oim', 'le-gueu', 'tit-pe', 'tass-pé', 'tard-pé', 'sser-ca', 'son-pri'], "femme" : ['celle-là', 'meuf', 'fe-meu', 'femme', 'elle', 'baby', 'bébé', 'nana', 'bonne', 'filles', 'girl', 'girlfriend', 'menteuse', 'bouffones', 'grosses'], "sanscategorie_reviennent_souvent" : ['sommeil', 'style', 'textes', 'dos', 'loin', 'weekend', 'système', 'jeu', 'nuit', 'nuits', 'vrai', 'pourquoi', 'yeux', 'poitrine', 'air', 'faut', 'prends', 'corps', 'histoires', 'face', 'game', 'crâne', 'choses', 'tête', 'croire', 'crois', 'fond', 'mêmes', 'toi', 'école', 'élève', 'important', 'essaye', 'vibe', 'inconnu'], "sanscategorie2" : ['attention', 'belek', 'folle', 'déteste', 'genre', "smokin'", 'avancer', 'bouteille', 'faux', 'faim', 'flow', 'flem', 'fois', 'jour', 'train', 'succès'], "sanscategorie3" : ['photos', 'coix', 'humeur', 'emoji', 'café', 'parler', 'pulsions', 'why', 'passe', 'choisi', 'peux', 'vice', 'connu', 'comprendre', 'demain', 'ennuies', 'refuses', 'longue', 'ligne', 'ko', 'hardcore', 'oublier', 'malade', 'traces'] }

def fusion_annee(ANNEE): 

        fichiers = [f for f in os.listdir(Path) if f.endswith(str(ANNEE)+".csv") and f.startswith("albums")]
        Nbfichiers = len(fichiers)
        if  Nbfichiers == 0:
            return 
        
        
        dic = OrderedDict()
        
        mots_restants = OrderedDict()
                    
        for path in fichiers: 
            with open(path, newline='', encoding='utf-8') as csvfile:
                linereader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in linereader:
                    word = row[0]
                    count = float(row[1])
                    appartenance = False
                    for key in champs_lexicaux.keys():
                        if word in champs_lexicaux[key]:
                            dic.update({word : (count, key)})
                            appartenance = True
                    if not appartenance :
                        mots_restants.update({word : count})
       
        dic = OrderedDict(sorted(dic.items(), key=lambda t: t[1][1]))      
        with open(Path+"\\champs_"+str(ANNEE)+".csv",  'w', newline='', encoding='utf-8') as csvfile:
            for key, value in dic.items():
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([key, value[0], value[1]])

        with open(Path+"\\champs_restants_"+str(ANNEE)+".csv",  'w', newline='', encoding='utf-8') as csvfile:
            for key, value in mots_restants.items():
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([key, value])
for annee in annees : 
    fusion_annee(2020)