from flask import Markup, url_for
from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele
from wtforms.fields import SelectField

class VueUtilisateur(VueModele) :

    can_create = True
    can_edit = True
    can_delete = True
    
    column_searchable_list = [
        'prenom',
        'nom',
        'telephone'
    ]


    column_exclude_list = [
        '_mdp'
    ]

    form_columns = [
        'civilite',
        'nom',
        'prenom',
        'telephone',
        'email',
        'notification_email',
        'notification_sms',
        'adresse'
        #'_mdp'
    ]

    form_overrides = dict(civilite=SelectField)
    form_args = dict(
    civilite=dict(
            choices=[( 'Mr','Monsieur'), ('Mme','Madame')]
   ))


class VueUtilisateurContact(VueUtilisateur):

    ''' Informations de contact de l'utilisateur. '''

    column_list = [
        'civilite',
        'nom',
        'prenom',
        'telephone',
        'email',
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
    VueUtilisateurContact(
        modeles.Utilisateur,
        db.session,
        endpoint='utilisateur/contact',
        category='Utilisateur',
        name='Contact',
        menu_icon_type='glyph',
        menu_icon_value='glyphicon-earphone'
    )
)


class VueUtilisateurCompte(VueUtilisateur):

    ''' Informations sur le compte de l'utilisateur. '''

    column_list = [
        'nom',
        'prenom',
        'telephone',
        'confirmation',
        'notification_email',
        'notification_sms',
        'avoir_compte',
        'inscription'
    ]


    column_filters = [
        'notification_email',
        'notification_sms',
        'avoir_compte'
    ]


admin.add_view(
    VueUtilisateurCompte(
        modeles.Utilisateur,
        db.session,
        endpoint='utilisateur/compte',
        category='Utilisateur',
        name='Compte',
        menu_icon_type='glyph',
        menu_icon_value='glyphicon-user'
    )
)



class VueUtilisateurBan(VueModele):

    ''' Informations sur le compte de l'utilisateur. '''

    
    can_create = True
    can_edit = True
    can_delete = True
    
    column_list = [
        'utilisateur',
        'debut',
        'fin',
        'raison'
    ]

    column_searchable_list = [
        'utilisateur'
    ]

    form_columns = [
    'utilisateur',
    'debut',
    'fin',
    'raison'
    ]

admin.add_view(
    VueUtilisateurBan(
        modeles.Bannissement,
        db.session,
        endpoint = 'utilisateur/bannissement',
        category = 'Utilisateur',
        name = 'Bannissement',
        menu_icon_type = 'glyph',
        menu_icon_value = 'glyphicon-remove'
    )
)