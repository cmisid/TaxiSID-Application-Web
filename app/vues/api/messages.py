from flask import Blueprint, render_template, jsonify
from app.vues.api import outils
from app import db


apimessagebp = Blueprint('apimessagebp', __name__, url_prefix='/api/messages')
    
@apimessagebp.route('/derniers_messages', methods=['GET','POST'])
def derniers_messages():
	''' Affiche les messages des dernières 24h. '''
	requete = db.session.execute("SELECT nom, prenom, TO_CHAR(moment,'HH24:MI') as date, sujet FROM messages M, conducteurs C WHERE M.conducteur = C.telephone AND moment > CURRENT_TIMESTAMP - interval '1 day' ORDER BY date DESC")
	return outils.transformer_json(requete)
 
@apimessagebp.route('/nouveau_message/telephone=<telephone>&message=<message>', methods=['GET','POST'])
def nouveau_message(telephone, message):
	''' Affiche les messages des dernières 24h. '''
	requete ="INSERT INTO messages VALUES ('{0}', CURRENT_TIMESTAMP, '{1}')".format(telephone, message)
	return outils.executer(requete)