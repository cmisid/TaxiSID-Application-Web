from flask import Markup, url_for
from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele

class VueStation(VueModele):

    ''' Informations sur les stations. '''

    can_create = True
    can_edit = True
    can_delete = True

    column_list = [
        'nom',
        'adresse',
        'distance_entree',
        'distance_sortie'
    ]

    column_searchable_list = [
    	'nom'
    ]

    form_columns = [
    	'nom',
    	'adresse',
    	'distance_entree',
    	'distance_sortie'
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
	VueStation(
		modeles.Station,
		db.session
	)
)