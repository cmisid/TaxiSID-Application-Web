from flask import Markup, url_for
from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele
from wtforms.fields import SelectField

categorie = 'Conducteur'

# Ajout penalité
# + oui non penalite


class VueConducteur(VueModele) :

    can_create = True
    can_edit = True
    can_delete = True

    column_searchable_list = [
        'nom',
        'prenom',
        'telephone'
    ]

    form_columns = [
        'civilite',
        'nom',
        'prenom',
        'telephone',
        'numero_imei',
        'email',
        'fax',
        'date_naissance',
        'adresse'
    ]

    form_overrides = dict(civilite=SelectField)
    form_args = dict(
    civilite=dict(
            choices=[( 'Mr','Monsieur'), ('Mme','Madame')]
   ))

class VueConducteurContact(VueConducteur):

    ''' Informations de contact du conducteur. '''
    
    
    column_list = [
        'civilite',
        'nom',
        'prenom',
        'telephone',
        'numero_imei',
        'email',
        'adresse',
        'inscription'
    ]


    def _lien_adresse(view, context, model, name):
        ''' Renvoyer le lien d'édition de l'adresse. '''
        lien = Markup(
            "<a href='{0}'>{1}</a>".format(
                url_for('adresse.edit_view', id=model.adresse),
                model.adresse
            )
        )
        return lien 

    column_formatters = {
        'adresse': _lien_adresse
    }

admin.add_view( 
    VueConducteurContact(
        modeles.Conducteur,
        db.session,
        endpoint='conducteur/contact',
        category='Conducteur',
        name='Contact',
        menu_icon_type='glyph',
        menu_icon_value ='glyphicon-earphone'
    )
)


class VueConducteurSituation(VueConducteur):

    ''' Informations sur la situation des conducteurs. '''

    column_list = [
        'civilite',
        'nom',
        'prenom',
        'telephone',
        'numero_imei',
        'statut',
        'station',
        'station_entree',
        'position'
    ]

    column_filters = [
        'statut',
        'station'
    ]

admin.add_view(
    VueConducteurSituation(
        modeles.Conducteur,
        db.session,
        endpoint='conducteur/situation',
        category ='Conducteur',
        name='Situation',
        menu_icon_type='glyph',
        menu_icon_value ='glyphicon-road'
    )
)


class VueConducteurPenalite(VueConducteur) :

    #colonnes à afficher
    column_list = [
        'civilite',
        'nom',
        'prenom',
        'telephone',
        'numero_imei',
        'fin_penalite'
        ]
      

admin.add_view(
    VueConducteurPenalite(
        modeles.Conducteur,
        db.session,
        endpoint='penalite',
        category='Conducteur',
        name='Pénalité',
        menu_icon_type='glyph',
        menu_icon_value ='glyphicon-remove'
    )
)