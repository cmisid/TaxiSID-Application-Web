# -*- coding: utf-8 -*-

from app import db


def test_trigger_verif_entreprises():

    db.session.execute("INSERT INTO courses(numero, depart, arrivee, entreprise) VALUES (999999999, 1,2,'ABA')")
	
    db.session.execute("INSERT INTO factures(course, montant) VALUES (999999999,16)")
    res = db.session.execute('SELECT montant FROM factures WHERE course = 999999999')
    val = []

    for row in res:
        val.append(row[0])
    
    print(val)
	
    assert val[0] == 16