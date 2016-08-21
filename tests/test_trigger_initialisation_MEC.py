# -*- coding: utf-8 -*-
"""
Fonction test
@author: Groupe 4
"""

from app import db
from app import modeles 
from datetime import datetime
import pytest

def test_trigger_initialisation_MEC():


	db.session.execute("INSERT INTO entreprises (nom, email, telephone, majoration, adresse)  VALUES ('ENT','test@mail.com','0512345678',10,3);")
	db.session.commit()


	res = db.engine.execute("SELECT montant_en_cours FROM entreprises WHERE nom = 'ENT';")
	val = []
	
	db.session.execute("DELETE FROM entreprises WHERE nom = 'ENT';")
	db.session.commit()

	for row in res:
		val.append(row[0])
		
	print(val)
	
	assert val[0] == 0	





		
	
		
	

