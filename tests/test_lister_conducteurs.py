# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 15:07:00 2016

@author: etudiant
"""

from app.attribution import lister_conducteurs

def test_definir_requete1():    
    assert '''SELECT C.telephone, C.station  FROM vehicules V, conducteurs C
                    WHERE V.conducteur = C.telephone
                    AND C.fin_penalite < current_timestamp 
                    AND V.places >= 1 AND lower(statut) in (lower('libre'), lower('destination')) AND V.animaux= True''' in lister_conducteurs.definir_requete(1, 2)

def test_definir_requete2():                  
    assert  '''SELECT C.telephone, C.station  FROM vehicules V, conducteurs C
                    WHERE V.conducteur = C.telephone
                    AND C.fin_penalite < current_timestamp 
                    AND V.places >= 1 AND lower(statut) in (lower('libre'), lower('destination')) AND V.animaux= True  AND V.vbreak = True  AND V.anglais = True''' in lister_conducteurs.definir_requete(1, 3, True, True)
                    
def test_definir_requete3():                  
    assert lister_conducteurs.definir_requete(1) == '''SELECT C.telephone, C.station  FROM vehicules V, conducteurs C
                    WHERE V.conducteur = C.telephone
                    AND C.fin_penalite < current_timestamp 
                    AND V.places >= 1 AND lower(statut) in (lower('libre'), lower('destination'))'''
                    
def test_definir_requete4():                  
    assert '''SELECT C.telephone FROM vehicules V, conducteurs C
                    WHERE V.conducteur = C.telephone
                    AND C.fin_penalite < current_timestamp 
                    AND V.places >= 1 AND lower(C.statut) = lower('libre')
                          AND lower(C.station) IN (lower('Capitole'), lower('Balma'))  AND V.animaux= True  AND V.vbreak = True  AND V.anglais = True ORDER BY C.station_entree; ''' in lister_conducteurs.definir_requete(1, 2, True, True, ['Capitole', 'Balma']) 