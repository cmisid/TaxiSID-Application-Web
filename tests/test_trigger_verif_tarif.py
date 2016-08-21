# -*- coding: utf-8 -*-

from app import db

def test_trigger_verif_tarif():

            db.session.execute("INSERT INTO forfaits(entreprise,destination_1,destination_2,tarif,montant) VALUES('ABA',1,3,'Jour',20.1)")
            db.session.commit()
            
            
            res = db.engine.execute("SELECT tarif FROM forfaits WHERE entreprise = 'ABA' AND destination_1 = 1 AND destination_2 = 3")
            val = []
            
            db.session.execute("DELETE FROM forfaits WHERE entreprise = 'ABA' AND destination_1 = 1 AND destination_2 = 3")
            db.session.commit()
            
            for row in res:
                val.append(row[0])
            
            print(val[0])
            
            # On vérifie que le tarif existe et est bien inséré
            assert val[0] == 'Jour'