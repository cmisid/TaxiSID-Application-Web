from flask import Blueprint, render_template, flash,jsonify, request 
from app import app, db, modeles
import psycopg2
import psycopg2.extras
import sys
import json
import unicodedata
from urllib.request import urlopen
from app.outils import utile
from app import modeles


# Créer un patron pour les vues conducteurs
conducteurbp = Blueprint('conducteurbp', __name__, url_prefix='/conducteur')

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


@conducteurbp.route('/<telephone>', methods=['GET', 'POST'])
def conducteur_accueil(telephone):
	''' Affiche la page d'accueil d'un conducteur. '''
	requete = db.session.execute("SELECT telephone, prenom, nom, ST_X(position) as lon, ST_Y(position) as lat, statut FROM conducteurs WHERE telephone = '{0}'".format(telephone))
	resultat = requete.first()
	conducteur = {
		'telephone': resultat[0],
		'prenom': resultat[1],
		'nom': resultat[2],
		'lat': resultat[3],
		'lon': resultat[4],
		'statut': resultat[5]
	}   
	return render_template('conducteur/accueil.html', titre='Conducteur', conducteur=conducteur)

@conducteurbp.route('/messages/<telephone>', methods=['GET'])
def conducteur_messages(telephone):
	''' Affiche les messages des dernières 24h. '''
	requete = db.session.execute("SELECT nom, prenom, TO_CHAR(moment,'HH24:MI') as date, sujet FROM messages M, conducteurs C WHERE M.conducteur = C.telephone AND moment > CURRENT_TIMESTAMP - interval '1 day' ORDER BY date DESC")
	lignes = requete.fetchall()
	nb_message = len(lignes);
	requete2 = db.session.execute("SELECT telephone, prenom, nom, ST_X(position) as lon, ST_Y(position) as lat, statut FROM conducteurs WHERE telephone = '{0}'".format(telephone))
	resultat = requete2.first()
	conducteur = {
		'telephone': resultat[0],
		'prenom': resultat[1],
		'nom': resultat[2],
		'lat': resultat[3],
		'lon': resultat[4],
		'statut': resultat[5]
	}
	return render_template('conducteur/messages.html', titre='Messages', messages=lignes,nb_message = nb_message, conducteur=conducteur)


@conducteurbp.route('/connexion/connexion', methods=['GET', 'POST'])
def connexion():
    return render_template('conducteur/connexion/connexion.html')


def load_json(string):
                # Fonction qui charge le contenu JSON
    return json.loads(string)
# Fin des fonctions de toolbox


@app.route('/gps', methods=['POST'])
def gps():
	string = request.data.decode()
	dt = json.loads(string)
	
# Fonction qui charge les données du trajet entre deux points (le départ est en lon,lat. L'arrivée en lon, lat ou textuelle)
	lonposition = dt['lonposition']
	latposition = dt['latposition']
	
#encoder l'adresse arriver
	adresse = dt['adresse']
	adresse = geocoder(adresse)
	adresse_arr = modeles.Adresse(
        position='POINT({0} {1})'.format(
            adresse['lat'],
			adresse['lon']
        )
    )
	latdestination = adresse['lat']
	londestination = adresse['lon']
	
#URL format
	mode = 'driving'
	base = 'https://maps.googleapis.com/maps/api/directions/json?'
	key = 'AIzaSyCBQSQ2Ze-8wEnZcT1V8__ug2WLdRmtdmA'
	lang = 'fr'
	a = '{lon},{lat}'.format(lat=latposition, lon=lonposition)
	b = '{lat},{lon}'.format(lat=latdestination, lon=londestination)
	url = '{0}origin={1}&destination={2}&language={3}&mode={4}&key={5}'.format(base, a, b, lang, mode, key)
	print(url)
#print(url)
	
	data = urlopen(url).read().decode('utf-8')
	jsonFile = load_json(data)
	
	AdressDep = jsonFile['routes'][0]['legs'][0]['start_address']
	AdressArr = jsonFile['routes'][0]['legs'][0]['end_address']
	steps = jsonFile['routes'][0]['legs'][0]['steps']
	distanceTot = jsonFile['routes'][0]['legs'][0]['distance']['text']
	durationTot = jsonFile['routes'][0]['legs'][0]['duration']['text']
	polyline = jsonFile['routes'][0]['overview_polyline']['points']

	return jsonify({
		'AdressDep': AdressDep,
		'AdressArr': AdressArr,
		'steps': steps,
		'distanceTot': distanceTot,
		'durationTot': durationTot,
		'polyline': polyline
	})

		
@conducteurbp.route('/informations/<telephone>', methods=['GET'])
def infos_stations(telephone):
	''' Affichage de la page informations(Stations, Conducteurs) '''
	stat_chauf=db.session.execute("select count(conducteurs.telephone) from conducteurs  right join stations on (conducteurs.station=stations.nom) group by stations.nom order by stations.nom")
	stat_chaufInf=stat_chauf.fetchall()
	stat = db.session.execute("select distinct nom from stations order by nom")
	statInf=stat.fetchall()
	lg = len(statInf)

	''' infos du chauffeur '''
	requete = db.session.execute("SELECT telephone, prenom, nom, ST_X(position) as lon, ST_Y(position) as lat, statut FROM conducteurs WHERE telephone = '{0}'".format(telephone))
	resultat = requete.first()
	conducteur = {
		'telephone': resultat[0],
		'prenom': resultat[1],
		'nom': resultat[2],
		'lat': resultat[3],
		'lon': resultat[4],
		'statut': resultat[5]
	}  

	return render_template('conducteur/informations.html', titre='Stations-Chauffeurs', stat_chaufInf=stat_chaufInf , statInf=statInf , lg=lg, conducteur=conducteur)


@conducteurbp.route('/courses/<telephone>', methods=['GET'])
def course_a_attribuer(telephone):
	''' Affichage de la page informations(Stations, Conducteurs) '''
	c0=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '0' and '0.59' ")
	c0=c0.fetchall()[0]
	c0=str(c0)[1]
	c1=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '1' and '1.59' ")
	c1=c1.fetchall()[0]
	c1=str(c1)[1]
	c2=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '2' and '2.59' ")
	c2=c2.fetchall()[0]
	c2=str(c2)[1]
	c3=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '3' and '3.59' ")
	c3=c3.fetchall()[0]
	c3=str(c3)[1]
	c4=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '4' and '4.59' ")
	c4=c4.fetchall()[0]
	c4=str(c4)[1]
	c5=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '5' and '5.59' ")
	c5=c5.fetchall()[0]
	c5=str(c5)[1]
	c6=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '6' and '6.59' ")
	c6=c6.fetchall()[0]
	c6=str(c6)[1]
	c7=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '7' and '7.59' ")
	c7=c7.fetchall()[0]
	c7=str(c7)[1]
	c8=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '8' and '8.59' ")
	c8=c8.fetchall()[0]
	c8=str(c8)[1]
	c9=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '9' and '9.59' ")
	c9=c9.fetchall()[0]
	c9=str(c9)[1]
	c10=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '10' and '10.59' ")
	c10=c10.fetchall()[0]
	c10=str(c10)[1]
	c11=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '11' and '11.59' ")
	c11=c11.fetchall()[0]
	c11=str(c11)[1]
	c12=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '12' and '12.59' ")
	c12=c12.fetchall()[0]
	c12=str(c12)[1]
	c13=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '13' and '13.59' ")
	c13=c13.fetchall()[0]
	c13=str(c13)[1]
	c14=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '14' and '14.59' ")
	c14=c14.fetchall()[0]
	c14=str(c14)[1]
	c15=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '15' and '15.59' ")
	c15=c15.fetchall()[0]
	c15=str(c15)[1]
	c16=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '16' and '16.59' ")
	c16=c16.fetchall()[0]
	c16=str(c16)[1]
	c17=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '17' and '17.59' ")
	c17=c17.fetchall()[0]
	c17=str(c17)[1]
	c18=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '18' and '18.59' ")
	c18=c18.fetchall()[0]
	c18=str(c18)[1]
	c19=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '19' and '19.59' ")
	c19=c19.fetchall()[0]
	c19=str(c19)[1]
	c20=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '20' and '20.59' ")
	c20=c20.fetchall()[0]
	c20=str(c20)[1]
	c21=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '21' and '21.59' ")
	c21=c21.fetchall()[0]
	c21=str(c21)[1]
	c22=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '22' and '22.59' ")
	c22=c22.fetchall()[0]
	c22=str(c22)[1]
	c23=db.session.execute("select count (numero) from courses where TO_CHAR(debut,'DD/MM/YYYY')=  TO_CHAR(now(),'DD/MM/YYYY') and extract(hour from debut) between '23' and '23.59' ")
	c23=c23.fetchall()[0]
	c23=str(c23)[1]

	''' infos du chauffeur '''
	requete = db.session.execute("SELECT telephone, prenom, nom, ST_X(position) as lon, ST_Y(position) as lat, statut FROM conducteurs WHERE telephone = '{0}'".format(telephone))
	resultat = requete.first()
	conducteur = {
		'telephone': resultat[0],
		'prenom': resultat[1],
		'nom': resultat[2],
		'lat': resultat[3],
		'lon': resultat[4],
		'statut': resultat[5]
	}  
	return render_template('conducteur/courses.html', titre='Courses à attribuer', conducteur = conducteur, c0=c0, c1=c1, c2=c2 ,c3=c3, c4=c4, c5=c5, c6=c6, c7=c7, c8=c8, c9=c9, c10=c10, c11=c11, c12=c12, c13=c13, c14=c14, c15=c15, c16=c16, c17=c19, c18=c18, c19=c19, c20=c20, c21=c21, c22=c22, c23=c23)

@conducteurbp.route('/details/<telephone>', methods=['GET'])
def detailsCourse(telephone):
	req=db.session.execute("select extract (hour from debut) as Tranches , numero , debut, depart, arrivee from courses where debut between  now() and now() + interval '24' hour group by numero order by tranches ")
	req=req.fetchall()
	leng = len(req)

	''' infos du chauffeur '''
	requete = db.session.execute("SELECT telephone, prenom, nom, ST_X(position) as lon, ST_Y(position) as lat, statut FROM conducteurs WHERE telephone = '{0}'".format(telephone))
	resultat = requete.first()
	conducteur = {
		'telephone': resultat[0],
		'prenom': resultat[1],
		'nom': resultat[2],
		'lat': resultat[3],
		'lon': resultat[4],
		'statut': resultat[5]
	}  
	return render_template('conducteur/details.html', titre='Courses du jour ', req=req, leng=leng, conducteur = conducteur)	
	
@conducteurbp.route('/infosDetaille/<telephone>', methods=['GET'])
def infosDetaille(telephone):
	req1=db.session.execute("select station, email, station_entree from conducteurs where   station_entree  between  now() and now() + interval '24' hour  ")
	req1=req1.fetchall()
	leng1 = len(req1)

	''' infos du chauffeur '''
	requete = db.session.execute("SELECT telephone, prenom, nom, ST_X(position) as lon, ST_Y(position) as lat, statut FROM conducteurs WHERE telephone = '{0}'".format(telephone))
	resultat = requete.first()
	conducteur = {
		'telephone': resultat[0],
		'prenom': resultat[1],
		'nom': resultat[2],
		'lat': resultat[3],
		'lon': resultat[4],
		'statut': resultat[5]
	}  

	return render_template('conducteur/infosDetaille.html', titre=' ', req1=req1, leng1=leng1, conducteur = conducteur)