from app.devis import calculer as ct
from datetime import datetime, timedelta

def test_calcul_ratios1():
	debut = datetime.now() + timedelta(days=1)
	fin = datetime.now() + timedelta(days=1, hours=5)
	duree = timedelta(0,18000,0)
	resultat = ct.ratios(debut, fin, duree)
	attente = {
		'nuit': 0,
		'jour': 1
	}
	assert 0 <= resultat['nuit'] <= 1
	
def test_calcul_ratios2():
	debut = datetime.now() + timedelta(days=1)
	fin = datetime.now() + timedelta(days=1, hours=5)
	duree = timedelta(0,18000,0)
	resultat = ct.ratios(debut, fin, duree)
	attente = {
		'nuit': 0,
		'jour': 1
	}
	assert 0 <= resultat['jour'] <= 1
	
def test_calcul_ratios3():
	debut = datetime.now() + timedelta(days=1)
	fin = datetime.now() + timedelta(days=1, hours=5)
	duree = timedelta(0,18000,0)
	resultat = ct.ratios(debut, fin, duree)
	attente = {
		'nuit': 0,
		'jour': 1
	}
	assert resultat['jour'] + resultat ['nuit'] == 1