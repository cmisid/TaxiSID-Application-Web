# -*- coding: utf-8 -*-
"""
Fonction test
@author: Groupe 2
"""

from app import db
from app import modeles 
from datetime import datetime
import pytest

def test_trigger_position_conducteur():
	db.session.execute("INSERT INTO conducteurs VALUES ('33333333334','nan','','aa@hotmail.fr','2016-02-11 09:22:34.743',10,'A','B','Inactif','Blagnac','2016-02-12 08:05:17.432001','01010000008E60884105CF4540008406AC6687F63F',34,'2016-01-12 08:05:17.0551','2017-01-12 08:05:17.0551')")
	db.session.commit()
	
	val_init = db.session.execute("SELECT position FROM conducteurs WHERE telephone = '33333333334';")

	db.session.execute("UPDATE conducteurs SET  position = '01010000005551BCCADACC4540C7A01342071DD66D' WHERE telephone = '33333333334';")
	db.session.commit()
	
	val_ajout = db.session.execute("SELECT position FROM positions WHERE conducteur = '33333333334' AND moment in (SELECT max(moment) FROM positions where conducteur = '33333333334');")
	
	val=[]
	for row in val_init:
		val.append(row[0])
		
	res=[]
	for row in val_ajout:
		res.append(row[0])
		
	db.session.execute("DELETE FROM positions WHERE conducteur = '33333333334';")
	db.session.commit()
	db.session.execute("DELETE FROM conducteurs WHERE telephone = '33333333334';")
	db.session.commit()

	
	assert res[0] == val[0]