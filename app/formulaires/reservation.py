from flask.ext.wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import (Required, Length, Email, ValidationError,
                                EqualTo)
from app.formulaires import validateurs as vd
from app.modeles import Adresse, Course, Utilisateur


class Demande_NonAuth(Form):
    ''' Demande de réservation d'un taxi par un utilisateur non-connecté. '''

    adresse_dep = TextField(
        validators=[vd.AdresseValide(Adresse, Adresse.adr_complete)], description='Adresse de départ')

    adresse_arr = TextField(
        validators=[vd.AdresseValide(Adresse, Adresse.adr_complete)], description="Adresse d'arrivée")

    nom = TextField(validators=[
        Required(message='Veuillez renseigner votre nom')
    ], description='Nom')

    prenom = TextField(validators=[
        Required(message='Veuillez renseigner votre prénom')
    ], description='Prénom')

    telephone = TextField(validators=[
        Required(message='Veuillez renseigner votre numéro de téléphone'), vd.verifierTelephone(
            Utilisateur, Utilisateur.telephone)
    ], description='Numéro de téléphone')

    mail = TextField(validators=[Email(
        message='Adresse email non valide')], description='Adresse email')

    civilite = SelectField('Civilité', choices=[
        ('monsieur', 'Monsieur'),
        ('madame', 'Madame')
    ])

    date_debut = TextField(validators=[
        Required(message='Veuillez renseigner une date de début'), vd.DateValide(
            Course, Course.debut)
    ], description='Date de début')

    nb_passagers = SelectField('Nombre de passagers', choices=[
        (str(i), str(i))
        for i in range(1, 9)
    ])

    paiement = SelectField('Paiement', choices=[
        ('especes', 'Espèces'),
        ('carte', 'Carte Bleue'),
        ('cheque', 'Chèque'),
        ('am_express', 'American Express')
    ])

    commentaire = TextField(description="Commentaire")

    nb_animaux = SelectField('Nombre animaux', choices=[
        (str(i), str(i))
        for i in range(0, 11, 1)
    ])
    nb_bagages = SelectField('Nombre de bagages éventuels', choices=[
        (str(i), str(i))
        for i in range(0, 6, 1)
    ])
    animaux_grands = SelectField("Pensez-vous que la taille de vos animaux nécessite d'avoir un grand véhicule ?", choices=[
        ('False', 'Non'),
        ('True', 'Oui'),
    ])

    langue = SelectField('Souhaitez-vous que le chauffeur parle anglais ?', choices=[
        ('False', 'Non'),
        ('True', 'Oui'),
    ])


class Demande_Auth(Form):

    ''' Demande de réservation d'un taxi par un utilisateur connecté. '''

    adresse_dep = TextField(
        validators=[vd.AdresseValide(Adresse, Adresse.adr_complete)], description='Adresse de départ')

    adresse_arr = TextField(
        validators=[vd.AdresseValide(Adresse, Adresse.adr_complete)], description="Adresse d'arrivée")

    date_debut = TextField(validators=[
        Required(message='Veuillez renseigner une date de début'), vd.DateValide(
            Course, Course.debut)
    ], description='Départ le')

    nb_passagers = SelectField('Nombre de passagers', choices=[
        (str(i), str(i))
        for i in range(1, 9)
    ])

    paiement = SelectField('Paiement', choices=[
        ('especes', 'Espèces'),
        ('carte', 'Carte Bleue'),
        ('cheque', 'Chèque'),
        ('am_express', 'American Express')
    ])

    commentaire = TextField(description="Commentaire")

    nb_animaux = SelectField('Nombre animaux', choices=[
        (str(i), str(i))
        for i in range(0, 11, 1)
    ])
    nb_bagages = SelectField('Nombre de bagages éventuels', choices=[
        (str(i), str(i))
        for i in range(0, 6, 1)
    ])
    animaux_grands = SelectField("Pensez-vous que la taille de vos animaux nécessite d'avoir un grand véhicule ?", choices=[
        ('False', 'Non'),
        ('True', 'Oui'),
    ])

    langue = SelectField('Souhaitez-vous que le chauffeur parle anglais ?', choices=[
        ('False', 'Non'),
        ('True', 'Oui'),
    ])
