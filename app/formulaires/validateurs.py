from wtforms import ValidationError
from app.outils import geographie
import datetime

class Unique(object):

    '''
    Validateur fait maison pour s'assurer qu'un
    attribut est unique. Par exemple on ne veut
    pas qu'un utilisateur puisse utiliser une
    adresse email qui a déjà été utilisé pour
    un autre compte. Cette classe suppose qu'on
    utilise SQLAlchemy.
    '''

    def __init__(self, model, field, message):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)


class AdresseValide(object):

    '''
    Validateur fait maison pour s'assurer qu'une
    adresse est valide. C'est à dire qu'on a
    réussi à la géocoder en lat/lon.
    '''

    def __init__(self, model, field):
        self.model = model
        self.field = field
        self.message = "Cette adresse n'est pas reconnue."

    def __call__(self, form, field):
        print(field.data)
        position = geographie.geocoder(field.data)
        if position['statut'] == 'echec':
            raise ValidationError(self.message)


class DateValide(object):

    '''
    Validateur fait maison pour s'assurer qu'une
    date est valide. C'est à dire qu'on vérifie qu'elle 
    est supérieure à la date actuelle.
    '''

    def __init__(self, model, field):
        self.model = model
        self.field = field
        self.message = "La date de réservation ne peut pas être antérieure à la date actuelle."

    def __call__(self, form, field):
        date_Aujd = datetime.datetime.now()
        date_Res = datetime.datetime.strptime(field.data, '%d-%m-%Y %H:%M')

        if date_Res < date_Aujd:
            print("True")
            raise ValidationError(self.message)


class verifierTelephone(object):
    ''' Validateur fait maison s'assurant qu'on a bien entré un numéro de téléphone. '''


    def __init__(self, model, field):
        self.model = model
        self.field = field
        self.message = "Les valeurs que vous avez entré ne correspondent pas à un numéro de téléphone."

    def __call__(self, form, field):
        telephone = field.data
        if len(telephone) != 10:
            raise ValidationError(self.message)

