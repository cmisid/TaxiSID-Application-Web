from flask import Markup, url_for
from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele
from wtforms.fields import SelectField

categorie = 'Entreprise'


class VueEntreprise(VueModele):

    ''' Informations sur les entreprise. '''
    
    can_create = True
    can_edit = True
    can_delete = True

    form_columns = [
        'nom',
        'email',
        'telephone',
        'majoration',
        'montant_en_cours',
        'adresse'
    ]

    column_list = [
        'nom',
        'email',
        'telephone',
        'majoration',
        'montant_en_cours',
        'adresse'
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
    VueEntreprise(
        modeles.Entreprise,
        db.session,
        endpoint='entreprise/contact',
        category='Entreprise',
        name='Contact',
        menu_icon_type='glyph',
        menu_icon_value ='glyphicon-earphone'
    )
)

class VueEntrepriseForfait(VueModele):

    ''' Informations sur les forfaits des entreprises. '''

    can_create = True
    can_edit = True
    can_delete = True

    column_list = [
        'entreprise',
		'destination_1',
		'destination_2',
		'tarif',
		'montant'
    ]

    column_searchable_list = [
        'entreprise',
        'destination_1',
        'destination_2',
        'tarif',
        'montant'
    ]

    form_columns = [
        'entreprise',
        'destination_1',
        'destination_2',
        'tarif',
        'montant'
    ]

    form_overrides = dict(tarif=SelectField)
    form_args = dict(
        tarif=dict(
            choices=[('jour', 'Jour'), ('nuit', 'Nuit')]
        ))

    def _lien_adresse(view, context, model, name):
        ''' Renvoyer le lien d'édition de l'adresse. '''
        lien = Markup(
            "<a href='{0}'>{1}</a>".format(
                url_for('adresse.edit_view', id=model.destination_1),
                model.destination_1
            )
        )
        return lien 

    def _lien_adresse1(view, context, model, name):
        ''' Renvoyer le lien d'édition de l'adresse. '''
        lien = Markup(
            "<a href='{0}'>{1}</a>".format(
                url_for('adresse.edit_view', id=model.destination_2),
                model.destination_2
            )
        )
        return lien 
        
    column_formatters = {
        'destination_1': _lien_adresse,
        'destination_2': _lien_adresse1
    }







admin.add_view(
    VueEntrepriseForfait(
        modeles.Forfait,
        db.session,
        endpoint='entreprise/forfaits',
        category ='Entreprise',
        name='Forfait',
        menu_icon_type='glyph',
        menu_icon_value ='glyphicon-euro'
    )
)