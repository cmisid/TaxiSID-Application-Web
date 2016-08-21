# -*- coding: utf-8 -*-
"""
@author: Groupe 6
Objectif : Différentes fonctions permettant de récupérer des informations 
sur la course.
Last Upate : 8/01/2016 13:00
"""

from app import db
from app.modeles import Course
from app.attribution import utiles


def information_course(numero):
    ''' Recupere des informations sur la course
    Parametre :
        numero :  Numéro de la course
    '''
    # Creation de la requete de selection des conducteurs
    result = db.session.query(Course).filter(Course.numero==numero).first()
    
    course = {}
    course['numero']  =  result.numero 
    course['places']  = result.places 
    course['animaux']  =  result.animaux  
    course['animaux_grands']  =  result.animaux_grands
    course['anglais'] = result.anglais
    course['depart'] = result.depart
    
    return(course)
    
# recup_depart
def position_depart(depart):
    ''' Fonction qui permet de recuperer les coordonnees du depart du client
    Parametres :
        depart : Point de départ du client (référencé dans la table adresse)
    '''
    # Recupération de la position de départ de la course
    query = ''' SELECT distinct ST_X(A.position) AS latitude, ST_Y(A.position) AS longitude
                FROM Adresses A
                WHERE A.identifiant = {depart_query} '''
                          
    # Creation et execution de la requête parametree
    query_param = query.format(depart_query=depart)
    result = db.engine.execute(query_param).fetchall()
    
    
    # Creation du dictionnare contenant les informations 
    coord_client = {}
    coord_client['latitude']  =  result[0][0] 
    coord_client['longitude']  =  result[0][1]
    
    return coord_client

def position_stations():
    ''' Recuperation des positions (lat,lon) de toutes le station
    '''
    
    # Recuperation des coordonnees (lat,lon) de chaque station, son rayon exterieur et son nom   
    query = ''' SELECT distinct ST_X(A.position) AS latitude, 
                                    ST_Y(A.position) AS longitude, 
                                    distance_sortie AS rayon, S.nom
                                    FROM Stations S, Adresses A
                                    WHERE S.Adresse = A.identifiant; '''
            
    # Stockage des resultats de la requête            
    result = db.engine.execute(query).fetchall()
    
    # Creation du dictionnare contenant les informations 
    coordonnees=[] 
    for position in result:
        coordonnees.append({'latitude' : position[0] , 'longitude' : position[1], 'rayon' : position[2], 'station' : position[3]})
        
    return coordonnees

def minimum_distance(liste_distance):
    ''' Fonction qui permet de recuperer le minimum des distances
    Parametres :
        liste_distance : liste des distance entre l'utilisateur et les stations
                            [{'station': 'value' , 'distance': value}]
    '''
    
    # Calcul du munimum
    minimum = min(liste_distance, key=lambda k: k['distance'])['distance']
    
    # Récupération des stations avec une distance minimum
    stations = []
    
    for element in liste_distance:
           if (element['distance'] == minimum) or (element['distance'] <= 0):
               stations.append(element['station'])
               
    return stations
    

def stations_proches(depart):
    ''' Fonction qui permet de trouver la station la plus proche de l'utilisateur
    Parametres :
        depart : adresse de depart du client
    '''
    depart = position_depart(depart)
    stations = position_stations()   
    
    # Calcul de la distance entre la station et l'utilisateur en metre   
    liste_distance=[]  
    for position in stations:
        temp = {'latitude': position['latitude'] , 'longitude': position['longitude']}
        dist_centre = utiles.calcul_distance(depart, temp)    
        dist_bor= dist_centre - position['rayon']
        liste_distance.append({'station' : position['station'], 'distance' : dist_bor})
        

    # Récupération des stations les plus proches 
    station_proche = minimum_distance(liste_distance)

    return station_proche             
     
            

    