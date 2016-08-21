from flask import Blueprint, render_template, jsonify
from app.vues.api import outils
from app import db, modeles
from app.outils import email


apiconducteurbp = Blueprint('apiconducteurbp', __name__, url_prefix='/api/conducteurs')

@apiconducteurbp.route('/adresses/<identifiant>', methods=['GET','POST'])
def adresse(identifiant):
    ''' Retourne les informations pour une certaine adresse. '''
    requete = db.session.execute("SELECT identifiant,nom_rue,numero,cp,ville,ST_X(position) as lat, ST_Y(position) as lon FROM adresses WHERE identifiant='{}'".format(identifiant))
    return outils.transformer_json(requete)

	
@apiconducteurbp.route('/<telephone>', methods=['GET','POST'])
def conducteur(telephone):
    ''' Retourne les informations pour un certain conducteur. '''
    requete = db.session.execute("SELECT * FROM conducteurs WHERE telephone='{}'".format(telephone))
    return outils.transformer_json(requete)

@apiconducteurbp.route('/imei=<imei>', methods=['GET','POST'])
def imei_telephone(imei):
    ''' Retourne le numéro de téléphone du conducteur avec pour paramètre le numéro imei. '''
    requete = db.session.execute("SELECT telephone FROM conducteurs WHERE numero_imei='{}'".format(imei))
    return outils.transformer_json(requete)

@apiconducteurbp.route('/propositions/<telephone>', methods=['GET','POST'])
def conducteur_propositions(telephone):
    ''' Retourne les propositions pour un certain conducteur. '''
    # Selection d'une course disponible pour le conducteur
    requete = db.session.execute("SELECT course FROM propositions WHERE conducteur = '{0}' AND statut IS NULL ".format(telephone))
    # Selection de la première course de la liste
    first_course_liste = requete.first()
    if not first_course_liste:
        return jsonify({'data' : [], 'statut' : 'echec'})
    else:
        first_course_var = first_course_liste[0]
        # Création d'une variable "nombre" pour savoir si le conducteur est prioritaire sur la course
        requete_2 = db.session.execute("SELECT COUNT(statut IS NULL) FROM propositions WHERE statut IS NULL AND ordre < (SELECT ordre FROM propositions WHERE conducteur = '{0}' AND course = '{1}') AND course = '{1}'".format(telephone, first_course_var))
        # Transformation de la requete en variable exploitable
        nombre_liste = requete_2.first()
        nombre = nombre_liste[0]
        if nombre == 0:
            detail_course = db.session.execute("SELECT * FROM courses WHERE numero = {}".format(first_course_var))
            return outils.transformer_json(detail_course)
        else:
            return jsonify({'data' : [], 'statut' : 'echec'})


@apiconducteurbp.route('/maj_statut/telephone=<telephone>&statut=<statut>', methods=['GET','POST'])
def conducteur_maj_statut(telephone, statut):
    ''' Met à jour le statut d'un conducteur dans la base de données. '''
    requete = "UPDATE conducteurs SET statut = '{0}' WHERE telephone = '{1}' ".format(statut, telephone)
    return outils.executer(requete)


@apiconducteurbp.route('/maj_position/telephone=<telephone>&lat=<lat>&lon=<lon>', methods=['GET','POST'])
def conducteur_maj_position(telephone, lat, lon):
    ''' Met à jour la position d'un conducteur dans la base de données. '''
    requete = "UPDATE conducteurs SET position = 'POINT({0} {1})' WHERE telephone = '{2}' ".format(lat, lon, telephone)
    return outils.executer(requete)


@apiconducteurbp.route('/accepter/numero=<numero>&course=<course>', methods=['GET','POST'])
def rep_oui(numero, course):
    ''' Le conducteur répond 'OUI' à la proposition de la course détaillée. '''
    try:
        # Affectation du conducteur à cette course dans la table courses
        db.session.execute("UPDATE courses SET conducteur = '{0}' WHERE numero = '{1}' ".format(numero, course))
        # Statut = 'Occupé' dans la table conducteurs pour ce conducteur
        db.session.execute("UPDATE conducteurs SET statut = 'Charge' WHERE telephone = '{}'".format(numero))
        db.session.commit()

        # Sujet de l'email
        sujet = "Confirmation de la prise en charge de votre course"
        # Corps de l'email
        corps = render_template('email/corps_email.html')
        # On récupère le numero de téléphone de l'utilisateur 
        requete = "SELECT u.telephone FROM utilisateurs u, courses c WHERE u.telephone = c.utilisateur AND c.numero = '{0}'".format(course)
        telephone = db.session.execute(requete).first()
        # On formate pour recuperer seulement le numero de telephone
        telephone = str(telephone)[2:13]
        # On récupere les informations de l'utilisateur avec en parametre le numero de telephone 
        utilisateur = modeles.Utilisateur.query.filter_by(
        telephone=telephone).first()
        # On envoye un email à l'utilisateur pour lui confirmer l'attribution de la course à un chauffeur
        email.envoyer(utilisateur.email, sujet, corps)
        return jsonify({'statut': 'succes'})
    except:
        return jsonify({'statut': 'echec'})

   
@apiconducteurbp.route('/refuser1/numero=<numero>&course=<course>', methods=['GET','POST'])
def rep_non_1(numero, course):
    '''
    Le conducteur répond 'NON' à une proposition de course.
    Le conducteur n'a pas le détail de cette course.
    '''
    try:
        # Mise à jour du statut pour refus de la course
        db.session.execute("UPDATE conducteurs SET statut ='Indisponible' WHERE telephone = '{0}'".format(numero))
		# Date et heure au moment de la réponse du conducteur dans la table propositions
        db.session.execute("UPDATE propositions SET reponse = CURRENT_TIMESTAMP WHERE conducteur = '{0}' AND course = '{1}'".format(numero, course))
        # Statut = 'Non' dans la table propositions pour ce conducteur et cette course
        db.session.execute("UPDATE propositions SET statut ='Non' WHERE conducteur = '{0}' AND course = '{1}'".format(numero, course))
        # Pénalité pour ce conducteur dans la table conducteurs
        db.session.execute("UPDATE conducteurs SET fin_penalite = CURRENT_TIMESTAMP + interval '2 minute' WHERE telephone = '{0}'".format(numero))
        db.session.commit()
        return jsonify({'statut': 'succes'})
    except:
        return jsonify({'statut': 'echec'})

     
@apiconducteurbp.route('/refuser2/numero=<numero>&course=<course>', methods=['GET','POST'])
def rep_non_2(numero, course):
    ''' Le conducteur répond 'NON' à la proposition de la course détaillée. '''
    try:
        # Pénalité pour ce conducteur dans la table conducteurs

        db.session.execute("UPDATE conducteurs SET fin_penalite = CURRENT_TIMESTAMP + interval '4 hour' WHERE telephone = '{0}'".format(numero))
        # Date et heure au moment de la réponse du conducteur dans la table propositions
        db.session.execute("UPDATE propositions SET reponse = CURRENT_TIMESTAMP WHERE conducteur = '{0}' AND course = '{1}'".format(numero, course))
        # Statut = 'Non' dans la table propositions pour ce conducteur et cette course
        db.session.execute("UPDATE propositions SET statut ='Non' WHERE conducteur = '{0}' AND course = '{1}'".format(numero, course))
        db.session.commit()
        dernier = db.session.execute("SELECT dernier FROM propositions WHERE conducteur = '{0}' AND course = '{1}'".format(numero, course))
        if dernier:
            attribuer_course(course)
        else:
            return jsonify({'statut': 'succes'})
        return jsonify({'statut': 'succes'})
    except:
        return jsonify({'statut': 'echec'})
		

@apiconducteurbp.route('/messages', methods=['GET','POST'])
def conducteur_messages():
    ''' Affiche les messages des dernières 24h. '''
    requete = db.session.execute("SELECT conducteur, TO_CHAR(moment,'DD/MM/YYYY HH:MI:SS') as date, sujet FROM messages WHERE moment > CURRENT_TIMESTAMP - interval '1 day' ORDER BY date DESC")
    return outils.transformer_json(requete)


@apiconducteurbp.route('/FinCourse/numero=<numero>&course=<course>', methods=['GET','POST'])
def FinCourse(numero, course):
    '''
    Le conducteur a fini une course.
    '''
    try:
        # Date et heure actualisées pour l'attribut station_entree dans la table conducteurs
        #db.session.execute("UPDATE courses SET finie = '1' WHERE telephone = '{}'".format(course))
        # Mise à jour du statut
        db.session.execute("UPDATE conducteurs SET statut ='Libre' WHERE telephone = '{0}'".format(numero, course))

        db.session.commit()
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'failure'})
