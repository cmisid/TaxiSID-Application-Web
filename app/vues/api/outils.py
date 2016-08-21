from flask import jsonify
from app.outils import sql
from app import db


def transformer_json(requete):
    ''' Transforme le resultat d'une requete en JSON. '''
    try:
        json = sql.to_dict(requete)
        return jsonify({'data': json, 'statut': 'succes'})
    except:
        return jsonify({'statut': 'echec'})


def executer(requete):
    ''' Execute une requete. '''
    try:
        db.session.execute(requete)
        db.session.commit()        
        return jsonify({'statut': 'succes'})
    except:
        return jsonify({'statut': 'echec'})