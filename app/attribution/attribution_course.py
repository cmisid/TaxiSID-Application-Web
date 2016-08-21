# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 10:52:46 2016

@author: Groupe 6
         Fonction final 
"""
from app.attribution import course
from app.attribution import insertion_propositions
from app.attribution import lister_conducteurs

def attribuer_courses_station(numero):
    ''' Proposer une liste de conducteurs disponibles dans la station
        pour une course
        Paramètres :
            numero : Numéro de la course
    '''
    # Récupération des informations sur la course
    information_course=course.information_course(numero)
    # stations concernees par la course 
    stations=course.stations_proches(information_course['depart'])
    
    # Liste tous les conducteurs disponibles (staut=libre) dans la ou les stations proches de la course
    conducteurs = lister_conducteurs.conducteurs_stations_disp(
            stations, information_course['places'], information_course['animaux'],
            information_course['animaux_grands'], information_course['anglais'] )
    
    
    if conducteurs == []:
        #Liste tous les conducteurs disponibles (statut=libre|occupé) dans la ou les stations proches de la course,
        conducteurs = lister_conducteurs.conducteurs_tous_disp(
                information_course['places'], information_course['animaux'], 
                information_course['animaux_grands'], information_course['anglais'])
        #Insertion dans la table Proposition, les conducteurs de la même station que le client
        insertion_propositions.inserer_conducteurs_toutes_station(numero, conducteurs, stations)
    else:        
        #Insertion dans la table Proposition, les conducteurs de la même station que le client.    
        insertion_propositions.inserer_conducteurs_meme_station(numero, conducteurs)
    
    
def attribuer_courses_tout(numero):
    ''' Proposer tous les conducteurs possibles pour une course
        numero : numero de la course
    '''
   # Récupération des informations sur la course
    information_course=course.information_course(numero)
    # stations concernees par la course 
    stations=course.stations_proches(information_course['depart'])
    
     #Liste tous les conducteurs disponibles (statut=libre|occupé) dans la ou les stations proches de la course,
    conducteurs = lister_conducteurs.conducteurs_tous_disp(
                information_course['places'], information_course['animaux'], 
                information_course['animaux_grands'], information_course['anglais'])
     #Insertion dans la table Proposition, les conducteurs de la même station que le client
    insertion_propositions.inserer_conducteurs_toutes_station(numero, conducteurs, stations)