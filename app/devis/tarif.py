from datetime import datetime, timedelta
from app.outils import geographie as geo
from app.outils import utile
from app.outils import calendrier
from app.devis import calculer
from app import app, db, modeles
from app.modeles import Course, Conducteur, Facture, Adresse
from geoalchemy2.functions import ST_AsGeoJSON
import json


def calculer_supplement(demande, supplements):
    ''' Calcul des suppléments. '''
    supplement = 0
    # Bagages
    supplement += int(demande['nb_bagages']) * supplements['bagage']
    # Animaux
    supplement += int(demande['nb_animaux']) * supplements['animal']
    # Passagers supplémentaires
    supplement += max(0, int(demande['nb_passagers']) - 4) * supplements['personne_sup']
    # Trajet à vide (ça ne m'a pas l'air bon, à discuter)
    supplement += supplements['trajet_a_vide']
    # Coût de prise en charge
    supplement += supplements['prise_en_charge']
    # Prise en charge à la gare
    if demande['gare'] is True:
        supplement += supplements['gare']
    # Prise en charge à l'aéroport
    if demande['aeroport'] is True:
        supplement += supplements['aeroport']


    return round(supplement,2)


def estimation(demande):
    ''' Calculer le devis d'une demande. '''

    # On récupère les tarifs applicables
    tarifs = utile.lire_json('app/devis/data/tarifs.json')
    supplements = utile.lire_json('app/devis/data/supplements.json')


    # Extraction des information de départ
    depart = geo.geocoder(demande['adresse_dep'])
    arrivee = geo.geocoder(demande['adresse_arr'])
    debut = demande['debut']

    # Simulation de la course
    simulation = calculer.simuler(depart, arrivee, debut)
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
        prix_par_km = tarifs['D']
    else:
        prix_par_km = jour * tarifs['C'] + nuit * tarifs['D']


    # Calculer le prix de la course
    montant = round(distance,1) * round(prix_par_km,2)


    # Calculer le supplément
    supplement = calculer_supplement(demande, supplements)

    # Tarif supplémentaire appliqué à un trajet ralenti (si temps de trajet plus long de 5 minutes 
    # par rapport à temps de trajet de référence, on applique une nouvelle tarification par minute de trajet supplémentaire)

    if round(simulation['ecart']/60) > 5:
        diff_minutes = round(simulation['ecart']/60) - 5
    else:
        diff_minutes = 0

    tarif_trajet_ralenti = diff_minutes * supplements['prix_trajet_ralenti']/60



    # Calcul du total minimum estimé
    total = montant + supplement + tarif_trajet_ralenti
    # Prise en compte du tarif minimum
    total = max(total, supplements['tarif_minimum'])


    # On retourne l'estimation à travers un dictionnaire de données

    estimation = {
        'prix': {
            'montant': round(montant, 2),
            'supplement': round(supplement, 2),
            'total': round(total,2)

        },
        'detail': {
            'parcours': {
                'duree': str(duree),
                'distance': round(distance,2),
                'prix_par_km': round(prix_par_km,2)
            },
            'bagages': {
                'nb': demande['nb_bagages'],
                'prix': supplements['bagage'],
                'total': round(int(demande['nb_bagages']) * supplements['bagage'],2)
            },
            'animaux': {
                'nb': demande['nb_animaux'],
                'prix': supplements['animal'],
                'total': round(int(demande['nb_animaux']) * supplements['animal'],2)
            },
            'personnes': {
                'nb': demande['nb_passagers'],
                'supplementaires': {
                    'nb': max(0, int(demande['nb_passagers']) - 4),
                    'prix': supplements['personne_sup'],
                    'total': round(max(0, int(demande['nb_passagers']) - 4) * supplements['personne_sup'],2)
                }
            },
            'gare': {
                'prise_en_charge': demande['gare'],
                'prix': 0 if not demande['gare'] else supplements['gare']
            },
            'aeroport': {
                'prise_en_charge': demande['aeroport'],
                'prix': 0 if not demande['aeroport'] else supplements['aeroport']
            },
            'prise_en_charge': supplements['prise_en_charge'],
            'tarif_trajet_ralenti' : round(tarif_trajet_ralenti,2),
            'trajet_a_vide':supplements['trajet_a_vide']
        }
    }
    return estimation




def estimation_precise(course):
    ''' Calculer le devis précis d'une course (en calculant le coût de trajet à vide). '''

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


    # On retourne la nouvelle estimation du prix du trajet
    return total
 

