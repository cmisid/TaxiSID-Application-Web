from flask import Blueprint, render_template
from app.vues.api import outils
from app import db


apibp = Blueprint('apibp', __name__, url_prefix='/api')


@apibp.route('/')
def api():
    return render_template('api.html', titre='API')


@apibp.route('/<table>', methods=['GET'])
def api_table(table):
    ''' Retourne n'importe quelle table dans la BD en format JSON. '''
    requete = db.session.execute("SELECT * FROM {}".format(table))
    return outils.transformer_json(requete)
