from flask import Blueprint, render_template, jsonify
from app.vues.api import outils
from app import db


apiadressebp = Blueprint('apiadressebp', __name__, url_prefix='/api/adresses')

@apiadressebp.route('/<identifiant>', methods=['GET','POST'])
def adresse(identifiant):
    ''' Retourne les informations pour une certaine adresse. '''
    requete = db.session.execute("SELECT * FROM adresses WHERE identifiant='{}'".format(identifiant))
    return outils.transformer_json(requete)