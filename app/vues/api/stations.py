from flask import Blueprint
from flask import jsonify
from app.vues.api import outils
from app.outils import sql
from app import db
from app import modeles
from datetime import datetime

apistationbp = Blueprint('apistationbp', __name__, url_prefix='/api/stations')



# Stations :
# Fonction qui renvoie adresse (ex : "001"), population par station (count chauffeurs), et res (je sais pas ce que c'est)
# Triés par adresse (ordre croissant)
@apistationbp.route('/getall/', methods=['GET'])
def getall():
    ''' Retourne les informations pour un certain conducteur. '''

    stations = modeles.Station.query.all()
    conducteurs = modeles.Conducteur.query.all()    
    data = [{
        'nom': station.adresse,
        'conducteurs': [
            {
                'conducteur': conducteur.telephone,
                'attente': round((datetime.now() - conducteur.station_entree).seconds / 60) if conducteur.station_entree else 'Nul'
            }
            for conducteur in conducteurs
            if conducteur.station == station.nom
        ]}
        for station in stations
    ]
    try:
        return jsonify({'data': data, 'statut': 'succes'})
    except:
        return jsonify({'statut': 'echec'})

#Info Population :
#Prends en paramètre une adresse de station
#Renvoie tous les taxi present sur l'adresse + temps qu'ils ont sont	
@apistationbp.route('/population/nom_station=<nom_station>', methods=['GET'])
def population():
    ''' Retourne les informations pour un certain conducteur. '''   
    requete = db.session.execute("select c.telephone, round((extract('epoch' from (CURRENT_TIMESTAMP - c.station_entree)))/60) temps from stations s, conducteurs c where c.station = s.nom and s.nom='<nom_station>'")
    json = outils.transformer_json(requete)
    return json


