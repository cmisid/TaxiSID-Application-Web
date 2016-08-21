import pandas as pd
from datetime import datetime
from app import db
from app import modeles
import random
from sqlalchemy import MetaData

# On vide les tables dans un ordre logique
modeles.Message.query.delete()
modeles.Notification.query.delete()
modeles.Forfait.query.delete()
modeles.Facture.query.delete()
modeles.Paiement.query.delete()
modeles.Etape.query.delete()
modeles.Proposition.query.delete()
modeles.Course.query.delete()
modeles.Vehicule.query.delete()
modeles.Position.query.delete()
modeles.Entreprise.query.delete()
modeles.Conducteur.query.delete()
modeles.Bannissement.query.delete()
modeles.Utilisateur.query.delete()

print('Tables vidées.')

########################
### Adresses Station ###
########################

def inserer_adresse_station(ligne):
    adresse = modeles.Adresse(
        position = 'POINT({0} {1})'.format(ligne['lat'], ligne['lon']),
        nom_rue = ligne['nom_rue'],
        numero = ligne['numero'],
        cp = ligne['cp'],
        ville = ligne['ville']
    )
    station = modeles.Station(
        nom = ligne['nom'],
        distance_entree = ligne['entree'],
        distance_sortie = ligne['sortie']
    )
    db.session.add(station)
    db.session.commit()
    db.session.add(adresse)
    db.session.commit()

    adresse.station = station.nom
    station.adresse = adresse.identifiant
    db.session.commit()

# On remet à neuf la clé qui s'auto-incrémente
db.session.execute('TRUNCATE TABLE adresses RESTART IDENTITY CASCADE;')
stations = pd.read_csv('app/data/stations.csv', encoding='utf8')
stations.apply(inserer_adresse_station, axis=1)

print('Adresses et stations insérées.')

####################
### Utilisateurs ###
####################

def inserer_utilisateur(ligne):
    utilisateur = modeles.Utilisateur(
	civilite = ligne['civilite'],
        prenom = ligne['prenom'].lower().capitalize(),
        nom = ligne['nom'].lower().capitalize(),
        email = ligne['email'],
        telephone = str(ligne['telephone']),
        confirmation = True,
        notification_sms = True,
        notification_email = True,
        inscription = datetime.utcnow(),
        adresse = ligne['adresse'],
        mdp = ligne['mdp'],
	avoir_compte = True
    )
    db.session.add(utilisateur)
    db.session.commit()

utilisateurs = pd.read_csv('app/data/utilisateurs.csv')
utilisateurs.apply(inserer_utilisateur, axis=1)

print('Utilisateurs insérés.')

########################################
############### Bannis #################
########################################

def inserer_banni(ligne):
    banni = modeles.Bannissement(
        utilisateur=str(ligne['utilisateur']),
        debut=ligne['debut'],
        fin=ligne['fin'],
	raison=ligne['raison']
    )
    db.session.add(banni)
    db.session.commit()

bannis = pd.read_csv('app/data/bannis.csv')
bannis.apply(inserer_banni, axis=1)

print('Bannis insérés.')

################################
### Véhicules et conducteurs ###
################################

def inserer_vehicule_conducteur(ligne):
    vehicule = modeles.Vehicule(
        immatriculation=ligne['immatriculation'],
        places=ligne['places'],
        couleur=ligne['couleur'],
        marque=ligne['marque'],
        animaux=ligne['animaux'],
        modele=ligne['modele'],
        american_express=ligne['american_express'],
        carte_bleue=ligne['carte_bleue'],
        cheque=ligne['cheque'],
        anglais=ligne['anglais'],
        espagnol=ligne['espagnol'],
        allemand=ligne['allemand'],
        vip=ligne['vip'],
        attelage=ligne['attelage'],
        vbreak=ligne['vbreak'],
        voiture_basse=ligne['voiture_basse'],
        mineur=ligne['mineur']
    )
    conducteur = modeles.Conducteur(
        telephone = str(ligne['telephone']),
        numero_imei= str(ligne['num_imei']),
        email = ligne['email'],
        civilite = ligne['civilite'],
        prenom = ligne['prenom'],
        nom = ligne['nom'],
	statut = ligne['statut'],
        station = ligne['station'],
        position = 'POINT({0} {1})'.format(ligne['lat'], ligne['lon']),
        adresse = ligne['adresse'],
        inscription = datetime.utcnow(),
	fin_penalite = datetime.utcnow()
    )
    db.session.add(vehicule)
    db.session.add(conducteur)
    db.session.commit()
    # Clés étangère (problème de l'oeuf de de la poule...)
    vehicule.conducteur = conducteur.telephone
    db.session.commit()

conducteurs = pd.read_csv('app/data/conducteurs.csv')
conducteurs.apply(inserer_vehicule_conducteur, axis=1)

print('Véhicules et conducteurs insérés.')

####################################
########### Entreprises ############
####################################

def inserer_entreprise(ligne):
    entreprise = modeles.Entreprise(
        nom = ligne['nom'],
        email = ligne['email'],
        telephone = str(ligne['tel']),
        majoration = ligne['majoration'],
        montant_en_cours = float(ligne['montant_en_cours']),
        adresse = ligne['adresse']
    )
        
    db.session.add(entreprise)
    db.session.commit()
        
entreprises = pd.read_csv('app/data/entreprises.csv')
entreprises.apply(inserer_entreprise, axis=1)

print('Entreprises insérées.')

########################################
############# Courses ##################
########################################

def inserer_course(ligne):
    course = modeles.Course(
        utilisateur = str(ligne['utilisateur']),
        finie = True,
        places = ligne['places'],
        priorite = ligne['priorite'],
        debut = ligne['debut'],
        commentaire = ligne['commentaire'],
        depart = ligne['depart'],
        arrivee = ligne['arrivee'],
	distance_estimee = ligne['distance_estimee'],
	bagages = ligne['bagages'],
	animaux = ligne['animaux'],
	animaux_grands = ligne['animaux_grands'],
	anglais = ligne['anglais']
	)
    if type(ligne['fin']) == str:
        course.fin = ligne['fin']
    if type(ligne['entreprise']) == str:
        course.entreprise = ligne['entreprise']
    if ligne['conducteur'] > 0:
        course.conducteur = str(int(ligne['conducteur']))
    db.session.add(course)
    db.session.commit()

db.session.execute('TRUNCATE TABLE courses RESTART IDENTITY CASCADE;')
courses = pd.read_csv('app/data/courses.csv')
courses.apply(inserer_course, axis=1)

print('Courses insérées.')

########################################
############# Factures #################
########################################

def inserer_facture(ligne):
	facture = modeles.Facture(
        course = ligne['course'],
        montant = ligne['montant'],
        type_paiement = ligne['type_paiement'],
        estimation_1 = ligne['estimation_1'],
        estimation_2 = ligne['estimation_2']
	)
	db.session.add(facture)
	db.session.commit()

db.session.execute('TRUNCATE TABLE factures RESTART IDENTITY CASCADE;')
factures = pd.read_csv('app/data/factures.csv')
factures.apply(inserer_facture, axis=1)

print('Factures insérées.')

########################################
############# Positions ################
########################################

def inserer_position(ligne):
    position = modeles.Position(
        conducteur = str(ligne['conducteur']),
        moment = ligne['moment'],
        position = 'POINT({0} {1})'.format(ligne['lat'], ligne['lon']),
    )
    db.session.add(position)
    db.session.commit()

positions = pd.read_csv('app/data/positions.csv')
positions.apply(inserer_position, axis=1)

print('Positions insérées.')

########################################
############### Etapes #################
########################################

def inserer_etape(ligne):
    etape = modeles.Etape(
        course = str(ligne['course']),
        moment = ligne['moment'],
        position = 'POINT({0} {1})'.format(ligne['lat'], ligne['lon']),
    )
    db.session.add(etape)
    db.session.commit()

etapes = pd.read_csv('app/data/etapes.csv')
etapes.apply(inserer_etape, axis=1)

print('Etapes insérées.')

####################################
########### Propositions ###########
####################################

def inserer_proposition(ligne):
    prop = modeles.Proposition(
        iteration = ligne['iteration'],
        course = ligne['course'],
        conducteur = str(ligne ['conducteur']),
        proposition = ligne['proposition'],
        reponse = ligne ['reponse'],
        statut = str(ligne ['statut']),
        raison = str(ligne ['raison']),
        ordre = ligne ['ordre']
    )
    
    db.session.add(prop)
    db.session.commit() 

propositions = pd.read_csv('app/data/propositions.csv', encoding='utf8')
propositions.apply(inserer_proposition, axis=1)

print('Propositions insérées.')

####################################
############# Forfaits #############
####################################

def inserer_forfait(ligne):
    forfait = modeles.Forfait(
        entreprise = ligne['entreprise'],
        destination_1= ligne['dest1'],
        destination_2 = ligne['dest2'],
        tarif = str(ligne['tarif']),
        montant = ligne['montant'],
    )
    
    db.session.add(forfait)
    db.session.commit()

forfaits = pd.read_csv('app/data/forfaits.csv')
forfaits.apply(inserer_forfait, axis=1)

print('Forfaits insérés.')

####################################
############ Paiements #############
####################################

def inserer_paiement(ligne):
    paiement = modeles.Paiement(
        entreprise = ligne['entreprise'],
        mois = ligne['mois'],
        annee = ligne['annee'],
        montant = ligne['montant']
    )
    db.session.add(paiement)
    db.session.commit()

paiements = pd.read_csv('app/data/paiements.csv', encoding='utf8')
paiements.apply(inserer_paiement, axis=1)

print('Paiements insérés.')

########################################
############# Messages #################
########################################

def inserer_message(ligne):
    message = modeles.Message(
        conducteur=str(ligne['conducteur']),
        moment=ligne['moment'],
        sujet=ligne['sujet'],
    )
    db.session.add(message)
    db.session.commit()

messages = pd.read_csv('app/data/messages.csv')
messages.apply(inserer_message, axis=1)

print('Messages insérés.')

########################################
############# Notifications ############
########################################

def inserer_notification(ligne):
    notification = modeles.Notification(
        utilisateur=str(ligne['utilisateur']),
        course=str(ligne['course']),
        moment=ligne['moment'],
	sujet=ligne['sujet']
    )
    db.session.add(notification)
    db.session.commit()

notifications = pd.read_csv('app/data/notifications.csv')
notifications.apply(inserer_notification, axis=1)

print('Notifications insérés.')
