# -*- coding: utf-8 -*-
"""
Fonction test
@author: Groupe 5
"""

from app import db
from app import modeles 
from datetime import datetime
import pytest

def test_trigger_initialisation_MEC():

	db.session.execute("UPDATE courses SET fin=null WHERE numero = 1")	
		
	res_etapes = db.session.execute("SELECT count(*) FROM etapes WHERE course = 1")
	val_etapes = []
	for row in res_etapes:
		val_etapes.append(row[0])
		
	res_factures = db.session.execute("SELECT count(*) FROM factures WHERE course = 1")
	val_factures = []
	for row in res_factures:
		val_factures.append(row[0])
		
	res_prop = db.session.execute("SELECT count(*) FROM propositions WHERE course = 1")
	val_prop = []
	for row in res_prop:
		val_prop.append(row[0])
		
	res_course = db.session.execute("SELECT count(*) FROM courses WHERE numero = 1")
	val_course = []
	for row in res_course:
		val_course.append(row[0])
		
	assert val_etapes[0] + val_course[0] + val_factures[0] + val_prop[0] == 0	





		
	
		
	

