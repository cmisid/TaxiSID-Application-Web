"""
Last Update on Wed 6 13:00:00 2016
Dernières modifications : ajout des fonctions convert_date et formatage_url
"""
from urllib.request import urlopen
import unicodedata
import time
import json
from datetime import datetime


def nettoyer(chaine):
    ''' Retirer les caractères spéciaux et les accents. '''
    texte = unicodedata.normalize('NFKD', chaine)
    octets = texte.encode('ascii', 'ignore')
    propre = octets.decode('utf-8')
    return propre


def requete_http(url, repetition=False):
    ''' Envoyez une requête et décoder les octets reçus. '''
    if repetition is False:
        with urlopen(url) as reponse:
            return reponse.read().decode('utf-8')
    # Possibilité de réessayer si la requête n'a pas fonctionné
    else:
        reponse = None
        while reponse is None:
            try:
                with urlopen(url) as reponse:
                    return reponse.read().decode('utf-8')
            except:
                reponse = None


def json_serial(obj):
    ''' Sérialiseur JSON pour les objets non sérialisables par défault par json '''

    # Si l'objet est de type datetime, alors on convertit la date en string
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial

    # Si le type n'est pas une date et n'est pas sériablisable on affiche
    # l'erreur
    raise TypeError("Type not serializable")


def ecrire_json(dictionaire, filename):
    ''' Ecrire un dictionaire dans un fichier JSON. '''
    with open(filename, 'w') as fichier:
        json.dump(dictionaire, fichier, default=json_serial)


def lire_json(filename):
    ''' Ouvrir un fichier JSON et le charger dans un dictionaire. '''
    with open(filename) as fichier:
        dictionaire = json.loads(fichier.read())
        return dictionaire


class MWT(object):
    ''' Memorize With Timeout. '''
    _caches = {}
    _timeouts = {}

    def __init__(self, timeout=2):
        self.timeout = timeout

    def collect(self):
        for func in self._caches:
            cache = {}
            for key in self._caches[func]:
                if (time.time() - self._caches[func][key][1]) < self._timeouts[func]:
                    cache[key] = self._caches[func][key]
            self._caches[func] = cache

    def __call__(self, f):
        self.cache = self._caches[f] = {}
        self._timeouts[f] = self.timeout

        def func(*args, **kwargs):
            kw = sorted(kwargs.items())
            key = (args, tuple(kw))
            try:
                v = self.cache[key]
                if (time.time() - v[1]) > self.timeout:
                    raise KeyError
            except KeyError:
                v = self.cache[key] = (f(*args, **kwargs), time.time())
            return v[0]
        func.func_name = f.__name__
        return func
    

def formatage_url(adresse):
    '''Fonction permettant de formater la chaîne de caractère.
    On remplace plusieurs espaces par un seul, puis les espaces par des +'''
    
    adresse = ' '.join(adresse.split())
    adresse = adresse.replace(' ','+')
   
    # Remplace les caractères spéciaux (accents, ponctuation ...)
    texte = unicodedata.normalize('NFKD', adresse)
    octets = texte.encode('ascii', 'ignore')
    adresse = octets.decode('utf-8')
    list_sc = [";",":","!",",",".","-","?","'","[","]","(",")","{","}"]
    adresse = ''.join([i if i not in list_sc else '' for i in adresse ])
   
   # Première lettre de l'adresse en majuscule  
    adresse = adresse.capitalize()
    return adresse
