from app.devis import calculer
from datetime import datetime, timedelta



def test_duree_trajet():
    depart = {
    'lat': 43.556368,
    'lon': 1.463929
    }

    arrivee = {
    'lat': 44.203142,
    'lon': 0.616363
    }
    resultat = calculer.duree_trajet(depart,arrivee,datetime.now() + timedelta(days=1))
    attente = {
            'duree': timedelta(0,4595),
            'distance': 124
        }
    assert resultat['distance'] == attente['distance']