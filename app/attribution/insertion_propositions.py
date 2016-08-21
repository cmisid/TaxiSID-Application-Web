# -*- coding: utf-8 -*-
"""
Fonction pour insérer les propositions dans la table Propositions
@author: Groupe 6
"""

from app import db
from app import modeles


def inserer_conducteurs_meme_station(numero, conducteurs):
    ''' Insertion dans la table Proposition, les conducteurs de la même station
    que le client.
    Paramètres :
        numero : numero de la course
        conducteurs : liste des conducteurs    
    '''
    
    # Insertion des propositions de course dans la table
    for i in range(0,len(conducteurs)):  
        if i==len(conducteurs)-1:
            proposition = modeles.Proposition(
                iteration=1, # Fixe
                course = numero,
                conducteur = conducteurs[i],
                ordre=i+1,
                meme_station = True,
                dernier = True
            )
        else:
            proposition = modeles.Proposition(
            iteration=1, # Fixe
            course = numero,
            conducteur = conducteurs[i],
            ordre=i+1,
            meme_station = True,
            dernier = False
        )
        db.session.add(proposition)
    db.session.commit()
    
def inserer_conducteurs_toutes_station(numero, conducteurs, station):
    ''' Insertion dans la table Proposition, tous les conducteurs diponibles
        Paramètres :
            numero : numero de la course
            conducteurs : liste des conducteurs [{'telephone' : num , 'station': nom}]
            station : station du client
        '''
    
    # Insertion des propostios de course dans la table
    for i in range(0,len(conducteurs)):
        
        # Est ce que le conducteur est dans la meme station que le client ?
        if station == conducteurs[i].get('station'):
                bool_course = True
        else:
                bool_course= False
                
        proposition = modeles.Proposition(
            iteration=2,
            course = numero,
            conducteur = conducteurs[i].get('telephone'),
            ordre=1,
            meme_station=bool_course,
            dernier = False
        )
        
        db.session.add(proposition)
    db.session.commit()