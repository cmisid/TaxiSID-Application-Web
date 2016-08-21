from app import db
from app import modeles 
from datetime import datetime
import pytest
from app.devis import tarif
from app.modeles import Course, Conducteur, Facture, Adresse
from app.outils import utile
import json
from geoalchemy2.functions import ST_AsGeoJSON
from app.devis import calculer
from app.outils import calendrier

course = {
    'numero': '11'
    }  

def test_estimation_precise ():
    db.session.execute("UPDATE courses SET conducteur='33624421417' WHERE numero = 11")
    
    # on récupère la valeur estimée de la course lors de la première estimation
    prix = db.session.query(Course,Facture).filter(Course.numero == Facture.course).filter(Course.numero == course['numero']).first()
    prix_estimation = prix.Facture.estimation_1


    # On récupère les tarifs applicables
    tarifs = utile.lire_json('app/devis/data/tarifs.json')
    supplements = utile.lire_json('app/devis/data/supplements.json')

    # On déduit au prix estimé la valeur de trajet à vide fixée dans la première estimation
    tav = supplements['trajet_a_vide']
    prix_estimation -= tav
    

    # Simulation du trajet à vide

    # Récupération de la position du taxi qui effectuera la course
    pos = db.session.query(Course,Conducteur).filter(Course.conducteur == Conducteur.telephone).filter(Course.numero == course['numero']).first()
    pos_taxi = pos.Conducteur.position
    position = json.loads(db.session.scalar(
                    ST_AsGeoJSON(
                        pos_taxi
                    )
                ))
    position['lat'] = position['coordinates'][0]
    position['lon'] = position['coordinates'][1]

    # Extraction des information de départ
    dep = db.session.query(Course,Adresse).filter(Course.depart == Adresse.identifiant).filter(Course.numero == course['numero']).first()
    depart = dep.Adresse.position
    adresse_dep = json.loads(db.session.scalar(
                    ST_AsGeoJSON(
                        depart
                    )
                ))

    adresse_dep['lat'] = adresse_dep['coordinates'][0]
    adresse_dep['lon'] = adresse_dep['coordinates'][1]
	
    depart_taxi = position
    depart_course = adresse_dep

    deb = db.session.query(Course,Adresse).filter(Course.numero == course['numero']).first()   
    debut = deb.Course.debut

    # Calcul de la distance
    simulation = calculer.simuler(depart_taxi, depart_course, debut)
    duree = simulation['duree']
    distance = simulation['distance']
    jour = simulation['ratios']['jour']
    nuit = simulation['ratios']['nuit']

    # Savoir si c'est un jour ferié ou un dimanche
    date = '{0}/{1}'.format(debut.day, debut.month)
    jours_feries = calendrier.feries(debut.year)
    ferie = date in jours_feries
    dimanche = debut.weekday() == 6

    # Décider du tarif à appliquer
    if ferie or dimanche:
        prix_par_km = tarifs['B']
    else:
        prix_par_km = jour * tarifs['A'] + nuit * tarifs['B']

    # Calculer le prix de la course
    total = round(prix_estimation + distance * prix_par_km,2)
    # Prise en compte du tarif minimum
    total = max(total, supplements['tarif_minimum'])
	
    print(total)
	
	
    resultat = tarif.estimation_precise(course)
    attente = total
    assert resultat == attente