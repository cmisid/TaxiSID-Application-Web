# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 23:56:30 2016

@author: etudiant
"""

from haversine import haversine

def formater_in_clause(liste):
    '''cette fonction permet de formater le liste des chauffeurs disponibles 
     de la (ou de les) station(s) sélectionné(s),'''
    liste_formate = '('
    first = True
    #parcourire le liste des chauffeurs disponibles dans une station 
    for element in liste:
        if first:
            first = False
        else:
             liste_formate=liste_formate + ", "
        liste_formate=liste_formate + "lower('" + element + "')"
                
    liste_formate = liste_formate + ')'
    
    return liste_formate

def calcul_distance(depart, arrivee):
    ''' Fonction qui permet de calculer la distance entre un depart et une arrivee
    Parametres :
        depart : Point de départ. Dictionnaire 
                    {'latitude': 'valeur' , 'longitude': 'valeur'}
        arrivee : Point d'arrivée. Dictionnaire
                    {'latitude': 'valeur' , 'longitude': 'valeur'}
    '''
    # Mise en forme des coordonnées sous forme d'une liste
    coord_depart=(depart['latitude'],depart['longitude'])
    coord_arrivee=(arrivee['latitude'],arrivee['longitude'])

    # Calcul de la distance
    distance  = haversine(coord_arrivee, coord_depart) * 1000
        
    return distance