from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele

class VueFacture(VueModele):

    ''' Informations sur les factures. '''

    can_create = True
    can_edit = True
    can_delete = True

    column_searchable_list = [
        'mois',
        'annee'
    ]

    form_columns = [
        'entreprise',
        'mois',
        'annee',
        'montant',
        'montant_majore'
    ]
    
    column_list = [
        'entreprise',
        'mois',
        'annee',
        'montant',
        'montant_majore'
    ] 

	

admin.add_view(
	VueFacture(
		modeles.Paiement,
		db.session
	)
)