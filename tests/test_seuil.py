from app.devis import calculer
from datetime import datetime

def test_seuil():
    date=datetime(2018,1,12,23,45)
    heure=8
    resultat = calculer.seuil(date,heure)
    attente=datetime(
        year=2018,
        month=1,
        day=12,
        hour=8
    )
    assert resultat == attente  