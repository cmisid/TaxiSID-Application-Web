import pandas as pd
import json
from geoalchemy2.functions import ST_AsGeoJSON
from app import db


def convertir_position(tableau, noms_colonnes=['position']):
    ''' Convertit un string PostGIS en latitude/longitude. '''
    for colonne in tableau:
        if colonne in noms_colonnes:
            geojson = [
                json.loads(db.session.scalar(
                    ST_AsGeoJSON(
                        position
                    )
                )) for position in tableau[colonne]
            ]
            tableau['lat'] = [position['coordinates'][0] for position in geojson]
            tableau['lon'] = [position['coordinates'][1] for position in geojson]
            tableau.drop(colonne, axis=1, inplace=True)
    return tableau


def securiser(tableau):
    ''' Retirer les colonnes secrètes d'un tableau pandas. '''
    for colonne in tableau:
        if colonne.startswith('_'):
            tableau.drop(colonne, axis=1, inplace=True)
    return tableau


def nettoyer(colonne):
    '''
    Nettoie une colonne d'un tableau pandas pour
    pouvoir la faire passer en JSON.
    '''
    # Convertir les dates au format ISO
    if colonne.dtype == 'datetime64[ns]':
        colonne = colonne.apply(lambda x: x.isoformat())
    # Convertir les booléens et NoneType en string
    if colonne.dtype == 'bool':
        colonne = colonne.apply(lambda x: 'True' if x is True else 'False')
    colonne = colonne.apply(lambda x: 'None' if x is None else x)
    return colonne


def to_dict(requete):
    ''' Transforme une requête SQL en dictionnaire. '''
    attributs = requete.keys()
    lignes = requete.fetchall()
    tableau = pd.DataFrame(lignes, columns=attributs)
    tableau = securiser(tableau)
    tableau = convertir_position(tableau)
    tableau = tableau.apply(nettoyer)
    json = tableau.to_dict(orient='records')
    return json
