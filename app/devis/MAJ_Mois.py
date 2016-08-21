from app.modeles import Entreprise, Paiement
from app import db
import datetime
import dateutil.relativedelta
#from apscheduler.schedulers.blocking import BlockingScheduler

def MAJ_mois():

    # On récupère le montant en cour de chaque entreprise
    entreprises = Entreprise.query.all()
    
    # On récupère le mois et l'année
    # On récupère le mois précédent
    date = datetime.datetime.now()
    mois_avant = date - dateutil.relativedelta.relativedelta(months=1)
    mois = mois_avant.month
    # On récupère l'année en cours
    annee = date.year
    # On récupère l'année précédente (utilisé si le mois précédent est décembre)
    annee_avant = date - dateutil.relativedelta.relativedelta(years=1)
    annee_avant = annee_avant.year
    
    # On insère les valeurs dans la table paiement   
    for entreprise in entreprises:
        if mois == 12:
            paiement = Paiement(
                entreprises = entreprise.nom,
                mois = mois,
                annee = annee_avant,
                montant = entreprise.montant_en_cours,
                montant_majore = entreprise.montant_en_cours * entreprise.majoration
            )
            print(paiement.montant)
            db.session.add(paiement)
            db.session.commit()
        else:
            paiement = Paiement(
                entreprises = entreprise.nom,
                mois = mois,
                annee = annee,
                montant = entreprise.montant_en_cours,
                montant_majore = entreprise.montant_en_cours * entreprise.majoration
            )
            db.session.add(paiement)
            db.session.commit()
        
    # On remet le montant en cour de l'entreprise à zéro
    db.session.execute ("""
    UPDATE entreprises
    SET montant_en_cour = 0""")
    
    # On met à jour la BD    
    db.session.commit()
 
# On utilise la fonction MAJ_mois tous les premiers de chaque mois                   
#sched = BlockingScheduler()
#sched.add_job(MAJ_mois, 'cron', month='*', day='1')
#sched.start()