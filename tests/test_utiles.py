# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:58:20 2016

@author: etudiant
"""

from app.attribution import utiles

def test_calcul_distance():
    #Test de la fonction calcul_distance
    DICO_DEPART={'latitude': 43.6040488, 'longitude': 1.44304740000007}
    DICO_ARRIVEE={'latitude': 43.598046,
                  'longitude': 1.431768,
                  'rayon': 1750.0,
                  'station': 'Aeroport'}
    assert  utiles.calcul_distance(DICO_DEPART,DICO_ARRIVEE) == 1127.141289748504
    
    
def test_formater_in_clause():
    #Test de la fonction formater_in_clause
    liste_formater=['a', 'b', 'c', 'd']
    assert utiles.formater_in_clause(liste_formater) == "(lower('a'), lower('b'), lower('c'), lower('d'))"