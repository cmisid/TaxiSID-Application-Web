from datetime import datetime, timedelta
from app.outils import calendrier
from app.outils import utile
from app.outils.distance import Parcours



def duree_trajet(depart, arrivee, debut):
    ''' Calculer la durée d'un trajet. '''
    
    # Initialiser un parcours
    parcours = Parcours(depart, arrivee, debut)
    # Calculer la durée du trajet
    parcours.calculer()

    # Obtenir l'estimation de la fin du trajet en datetime
    duree = timedelta(minutes=parcours.duree) / 60
    distance = round(parcours.distance / 1000)
    return {
        'duree': duree,
        'distance': distance
    }


def seuil(date, heure):
    ''' Retourne un seuil en format datetime. '''
    seuil = datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=heure
    )
    return seuil


def ratios(debut, fin, duree):
    ''' Calcul des ratios jour/nuit. '''

    # Obtenir les seuils de début et de fin
    seuil_jour_debut = seuil(debut, heure=8).timestamp()
    seuil_jour_fin = seuil(fin, heure=8).timestamp()
    seuil_nuit_debut = seuil(debut, heure=19).timestamp()
    seuil_nuit_fin = seuil(fin, heure=19).timestamp()

    # Convertir les datetime en timestamp pour les comparer aux seuils
    debut = debut.timestamp()
    fin = fin.timestamp()

    # On pourra obtenir le temps passé la nuit à partir de celui passé le jour
    duree_jour = 0

    # La course commence pendant la journée du jour de départ
    if seuil_jour_debut < debut < seuil_nuit_debut:
        # La course finit pendant la journée du jour de départ
        if fin < seuil_nuit_debut:
            duree_jour += fin - debut
        # La course finit pendant la nuit du jour de départ
        else:
            duree_jour += seuil_nuit_debut - debut
    # La course finit durant la journée du lendemain du jour de départ
    if seuil_jour_debut < seuil_jour_fin < fin:
        duree_jour += fin - seuil_jour_fin
    # La course commence pendant la nuit
    if debut < seuil_jour_debut:
        # La course finit pendant la journée du même jour
        if fin > seuil_jour_debut:
            duree_jour += fin - seuil_jour_debut

    # Déduire les ratios jour/nuit
    ratio_jour = duree_jour / duree.seconds
    ratio_nuit = 1 - ratio_jour
    return {
        'jour': round(ratio_jour,2),
        'nuit': round(ratio_nuit,2)
    } 
    

def simuler(depart, arrivee, debut):
    '''
    Trouver la duree d'une course
    et le temps passé pendant le jour ou la nuit
    d'une course.
    '''

    # Calculer la durée du trajet
    course = duree_trajet(depart, arrivee, debut)
    duree = course['duree']
    distance = course['distance']


    # Choisir une date de départ de référence (avec peu de trafic) pour calculer le temps passé en tarif ralenti

    reference_debut = datetime(
        year=debut.year,
        month=debut.month,
        day=debut.day,
        hour=10
    ) + timedelta(days=7)

    
    # Calculer la durée du trajet de référence
    reference = duree_trajet(depart, arrivee, reference_debut)
    reference_duree = reference['duree']


    fin = debut + duree

    ecart = abs(duree - reference_duree).seconds

    return {
        'duree': duree,
        'distance': distance,
        'ratios': ratios(debut, fin, duree),
        'ecart': ecart
    }
