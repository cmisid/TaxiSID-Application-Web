from app.devis import calculer
from datetime import datetime, timedelta


def test_simuler():
    depart = {
    'lat': 43.556368,
    'lon': 1.463929
    }

    arrivee = {
    'lat': 44.203142,
    'lon': 0.616363
    }
    
    debut = datetime(2050,12,1)
    
    resultat = calculer.simuler(depart,arrivee,debut)
    #attente = {
       #     'duree': timedelta(0,4497),
        #    'ecart': 115,
         #   'distance': 124,
          #  'ratios': {
           #         'nuit': 1.0,
           #         'jour': 0.0
            #    }
       # }
    assert resultat['ecart'] < 150