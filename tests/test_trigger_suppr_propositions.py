# -*- coding: utf-8 -*-
"""
Fonction test
@author: Groupe 5
"""

from app import db
from app import modeles 
from datetime import datetime
import pytest

def test_trigger_suppr_propositions():

	db.session.execute("UPDATE courses SET conducteur = NULL WHERE numero = 10");
	db.session.execute("INSERT INTO propositions (course, conducteur, proposition, reponse) VALUES (10,'33608871046', '2016-02-14 06:43:20.3944', '2016-02-16 06:43:20.3944');")
	db.session.execute("INSERT INTO propositions (course, conducteur, proposition, reponse) VALUES (20,'33614535685', '2016-02-14 06:43:20.3944', '2016-02-16 06:43:20.3944');")
	db.session.execute("INSERT INTO propositions (course, conducteur, proposition, reponse) VALUES (10,'33614535685', '2016-02-14 06:43:20.3944', '2016-02-16 06:43:20.3944');")
	db.session.execute("UPDATE courses SET conducteur = '33614535685' WHERE numero = 10;")
	
	res = db.session.execute("SELECT count(*) FROM propositions WHERE course = 10;")
	val = []	
	for row in res:
		val.append(row[0])

	res1 = db.session.execute("SELECT count(*) FROM propositions WHERE conducteur = '33614535685';")
	valeur = []
	for rows in res1:
		valeur.append(rows[0])
	
	assert valeur[0] + val[0] == 0