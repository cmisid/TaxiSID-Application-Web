from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import (
    Required, Length, Email, ValidationError, EqualTo)
from app.modeles import Utilisateur
from app.formulaires import validateurs


class Oubli(Form):

    ''' Oubli de mot de passe. '''

    email = TextField(validators=[Required(), Email()],
                      description='Adresse email')


class Reinitialisation(Form):

    ''' Reinitisation de mot de passe. '''

    mdp = PasswordField(validators=[Required(), Length(min=6),
                                    EqualTo('confirmation', message='Les mots de passe doivent être ' + 'identiques.')],
                        description='Nouveau mot de passe')

    confirmation = PasswordField(
        description='Confirmer le nouveau mot de passe')


class Connexion(Form):

    ''' Connexion. '''

    email = TextField(
        validators=[Required(), Email()], description='Adresse email')
    mdp = PasswordField(validators=[Required()], description='Mot de passe')


class Enregistrement(Form):

    ''' Enregistrement. '''

    prenom = TextField(
        validators=[Required(), Length(min=2)],
        description='Prénom')

    nom = TextField(
        validators=[Required(), Length(min=2)],
        description='Nom')

    telephone = TextField(validators=[
        Required(message='Veuillez renseigner votre numéro de téléphone'), validateurs.verifierTelephone(
            Utilisateur, Utilisateur.telephone)
    ], description='Numéro de téléphone')

    email = TextField(
        validators=[Required(), Email()],
        description='Adresse email')

    civilite = SelectField('Civilité', choices=[
        ('monsieur', 'Monsieur'),
        ('madame', 'Madame')
    ])

    ville = TextField(description='Ville')

    cp = TextField(description='Code postal', validators=[Length(max=5)])

    adresse = TextField(description='Adresse')

    numero = TextField(description='Numéro')

    mdp = PasswordField(
        validators=[Required(), Length(min=6), EqualTo(
            'confirmation', message='Les mots de passe doivent être identiques.')],
        description='Mot de passe')

    confirmation = PasswordField(description='Confirmer le mot de passe')


class Modification(Form):

    ''' Edition des données de l'utilisateur. '''

    prenom = TextField(
        validators=[Required(), Length(min=2)], description='Prénom')
    nom = TextField(validators=[Required(), Length(min=2)], description='Nom')
    telephone = TextField(validators=[Required(), Length(
        min=6)], description='Numéro de téléphone')


class Contact(Form):

    ''' Envoi d'un email. '''

    prenom = TextField(
        validators=[Required(), Length(min=2)],
        description='Prénom')

    nom = TextField(
        validators=[Required(), Length(min=2)],
        description='Nom')

    email = TextField(
        validators=[Required(), Email()], description='Adresse email')

    objet = TextField(
        validators=[Required(), Length(min=2)],
        description='Objet de votre message')

    sujet = TextField(
        validators=[Required(), Length(min=2)],
        description='Entrez ici le corps de votre message')
