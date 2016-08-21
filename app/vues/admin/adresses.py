from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele

class VueAdresse(VueModele):

    can_create = True
    can_edit = True
    can_delete = True

    form_columns = [
        'numero',
    	'nom_rue',
    	'cp',
    	'ville'
    ]

    column_list = [
	'identifiant',
    'numero',
    'nom_rue',
    'cp',
    'ville',
    'adr_complete',
    'station'
    ]

admin.add_view(
	VueAdresse(
		modeles.Adresse,
		db.session
	)
)
