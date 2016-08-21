from flask import request, Response
from werkzeug.exceptions import HTTPException
from flask_admin.contrib.geoa import ModelView
from app import app


class VueModele(ModelView):
    '''
    Vue de base qui implémente une authentification
    HTTP. Toutes les autres vues héritent de celle-ci.
    '''

    list_template = 'admin/list.html'
    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'

    # Edition des données dans une fenêtre modale
    #create_modal = True
    #edit_modal = True

    # Afficher la clé primaire dans les vues
    column_display_pk = True

    # Configuration pour afficher les liens
    column_hide_backrefs = False
    column_display_all_relations = True
    column_auto_select_related = True

    def is_accessible(self):
        auth = request.authorization or request.environ.get(
            'REMOTE_USER')  # workaround for Apache
        if not auth or (auth.username, auth.password) != app.config['ADMIN_CREDENTIALS']:
            message = 'Il faut rentrer les identifiants administrateur.'
            raise HTTPException('', Response(message, 401, {
                'WWW-Authenticate': 'Basic realm="Identifiants requis"'
            }))
        return True
