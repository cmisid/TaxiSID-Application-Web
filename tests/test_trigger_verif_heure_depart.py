# -*- coding: utf-8 -*-
"""
Fonction test
@author: Groupe 2
"""

from app import db
from app import modeles 
from datetime import datetime
import pytest

def test_trigger_verif_heure_depart():
	with pytest.raises(Exception) as excinfo:
		def test_heure_depart():
			db.session.execute("INSERT INTO courses(utilisateur, conducteur, places, priorite, debut, fin, commentaire, depart, arrivee) VALUES ('33628251338','33699428430', 4, 'high', '2016-01-11 02:03:04.3256', '2016-01-12 04:03:04.3256', 'Haha', 1,2)")

		test_heure_depart()

		
	assert 'L\'heure de depart de la course doit etre posterieure a l\'heure de la commande\n' in str(excinfo.value)
	
	