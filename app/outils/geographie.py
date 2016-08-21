import json
from app.outils import utile
from haversine import haversine


@utile.MWT(timeout=60 * 60 * 24)
def geocoder(adresse):
    '''
    Geocoder une adresse en (latitude, longitude) grâce à
    l'API de Nominatim.
    '''
    base = 'http://nominatim.openstreetmap.org/search?' \
           'format=json&polygon_geojson=1&q='
    texte = utile.nettoyer(adresse)
    mots_cles = '+'.join(texte.split())
    url = ''.join((base, mots_cles))
    reponse = utile.requete_http(url)
    try:
        adresse = json.loads(reponse)[0]
        latitude = float(adresse['lat'])
        longitude = float(adresse['lon'])
        return {
            'statut': 'succes',
            'lat': latitude,
            'lon': longitude
        }
    # L'adresse n'est pas valide
    except:
        return {
            'statut': 'echec'
        }


def calculer_distance(adresse_dep, adresse_cible, rayon):
    ''' On géocode deux adresses et on regarde si la distance entre les deux est 
    inférieure à un rayon représentant la zone de l'adresse_cible (gare ou aéroport) '''
    adr_dep = geocoder(adresse_dep)
    coord_dep = (adr_dep['lat'], adr_dep['lon'])

    adr_cible = geocoder(adresse_cible)
    coord_cible = (adr_cible['lat'], adr_cible['lon'])

    dist_centre = haversine(coord_dep, coord_cible) * 1000

    if dist_centre - rayon <= rayon:
        return True
    else:
        return False
