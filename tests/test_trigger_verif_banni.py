# -*- coding: utf-8 -*-
"""
Fonction test
@author: Groupe 2
"""

from app import db
from app import modeles 
from datetime import datetime
import pytest

def test_trigger_banni():
	with pytest.raises(Exception) as excinfo:
		
		db.session.execute("INSERT INTO utilisateurs(telephone, civilite, email, confirmation, prenom, nom, notification_email, notification_sms, inscription, adresse, _mdp) VALUES ('3362824526', 'Mme','lzl@lo.fr', TRUE, 'A', 'B', TRUE, TRUE, CURRENT_DATE, 2, 'loulou')")
		db.session.execute("INSERT INTO bannissements values('3362824526','05/01/2017','06/01/2019','Impolitesse')")
		db.session.execute("INSERT INTO courses(utilisateur, conducteur, places, priorite, debut, fin, commentaire, depart, arrivee) VALUES ('3362824526','33699428430', 4, 'high', '2017-02-11 02:03:04.3256', '2017-02-12 04:03:04.3256', 'Haha', 1,2)")
		
	assert 'l\'utilisateur est actuellement bannit\n' in str(excinfo.value)	