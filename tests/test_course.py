# -*- coding: utf-8 -*-
"""
Éditeur de Spyder
Auteur : Groupe 6
Objectif : Tester la fonction qui permet ..........
"""


from app.attribution import course
#from app.attribution import utiles
from app import db

##Tests

def test_information_course():
    db.session.execute("INSERT INTO courses(numero, animaux, animaux_grands, places, anglais, depart) VALUES ('100', 1 , False, 2, False, 1)")
    db.session.commit()

    assert course.information_course(100) == {'numero': 100, 'places':2, 'animaux': 1, 'animaux_grands': False, 'anglais':False, 'depart':1}
    
    db.session.execute("DELETE FROM courses WHERE numero = 100")
    db.session.commit()

    
def test_position_depart():
	db.session.execute("INSERT INTO adresses(identifiant, nom_rue, numero, cp, ville, position) VALUES (101,'Place Esquirol',12.0,31000,'Toulouse','01010000005551BCCADACC4540C7A01342071DF73F')")
	db.session.commit()
   
	assert course.position_depart(101) == {'latitude': 43.600427, 'longitude': 1.444587}

	db.session.execute("DELETE FROM adresses WHERE identifiant = 101")
	db.session.commit()

 
def test_minimum_distance():
   
	liste_distance=[{'distance':15 , 'station': 'U3-218'},{'distance':150 , 'station': 'U3-208'}]
	assert  course.minimum_distance(liste_distance) == ['U3-218']

