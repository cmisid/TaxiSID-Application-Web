# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 11:06:34 2016

@author: Groupe 6
"""
from app import db
from app.attribution import utiles

def definir_requete(places, animaux = 0, animaux_grands = False, anglais= False, liste_stations = []):
    
    # Construction de la requête    
    query='''SELECT C.telephone'''
    
    if(liste_stations == []):
        # Si pas de stations, récupérer la station du conducteur
       query = query + ''', C.station '''

    # Spécification des tables, des conditions de jointure, des banissements et 
    # du nombre de place disponible   
    query= query + ''' FROM vehicules V, conducteurs C
                    WHERE V.conducteur = C.telephone
                    AND C.fin_penalite < current_timestamp 
                    AND V.places >= {places_query} '''
                    
    # Si pas de stations, récupérer les conducteurs 'libre' et 'occupé'       
    if (liste_stations == []):
       query = query +    '''AND lower(statut) in (lower('libre'), lower('destination'))'''
    # Sinon récupérer seulement les conducteurs 'libre' de la station
    else:
       query = query + '''AND lower(C.statut) = lower('libre')
                          AND lower(C.station) IN {station} '''
            
    # Prise en compte de animaux                 
    if (animaux>0):
       query = query + ''' AND V.animaux= True '''

    # Si il y a des gros animaux    
    if (animaux_grands):
       query = query + ''' AND V.vbreak = True '''
      
    if (anglais):
        query = query + ''' AND V.anglais = True'''

    # Si on recherche les conducteurs de la station, les ordonner par ordre d'arrivée    
    if(liste_stations != []):
       query = query + ''' ORDER BY C.station_entree; '''
    
    query_param=''
    if(liste_stations != []):
        # Formate la liste des stations pour la clause IN
       liste_stations_format=utiles.formater_in_clause(liste_stations)
        # Création et execution de la requête parametrée
       query_param = query.format(station=liste_stations_format, places_query=places, anglais_query=anglais)
    else:
       # Création et execution de la requête parametrée
       query_param = query.format(places_query=places, anglais_query=anglais)   

    return query_param


def conducteurs_stations_disp(liste_stations, places, animaux=0, animaux_grands=False, anglais=False):
    ''' Liste tous les conducteurs disponibles (statut=libre) dans la ou les 
    stations proches de la course, respectant différents critères.
    Les conducteurs sont triés par ordre d'arrivée dans la station.
    Paramètres :
        liste_stations : Liste contenant des noms de station.
        places : Nombre de passagers minimum
        animaux : Nombre d'animaux
        animaux_grands : La course contient-elle des grands animaux ?
        anglais : Anglais obligatoire pour le conducteur
    Sorties :
        Retourne la liste des conducteurs disponibles dans la (les) station(s) 
        placée(s) en paramètre
    '''
    # Construction de la requête
    query = definir_requete(places, animaux, animaux_grands, anglais, liste_stations)
    result = db.engine.execute(query)   
    results=[]
    
    # Ajout des résultats dans une liste
    for row in result: 
        results.append(row['telephone'])
    
    return results


def conducteurs_tous_disp(places, animaux=0, animaux_grands=False, anglais=False):
    ''' Liste tous les conducteurs disponibles (statut=libre|occupé) 
    dans la ou les stations proches de la course, respectant différents critères.
    Paramètres :
        places : Nombre de passagers minimum
        animaux : Defaut = false
        animaux_grands : La course contient-elle des grands animaux ?
        anglais : Anglais obligatoire pour le conducteur
    Sorties :
        Retourne la liste des conducteurs disponibles dans les 
        différentes stations [[{'telephone' : num , 'station': nom}]
    '''
    # Construction de la requête
    query = definir_requete(places, animaux, animaux_grands, anglais)
    result = db.engine.execute(query)   
    results=[]
    
    # Ajout des résultats dans une liste
    for row in result: 
        results.append({'telephone' : str(row['telephone']), 'station':str(row['station'])})

    return results
