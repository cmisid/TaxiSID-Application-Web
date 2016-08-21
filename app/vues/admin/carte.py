from flask import jsonify
from flask.ext.admin import BaseView, expose
from geoalchemy2.functions import ST_AsGeoJSON
import json
from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele

class VueCarte(BaseView):
    
    # Données de la carte
    @expose('/')
    def index(self):
        return self.render('admin/carte.html')

    @expose('/rafraichir', methods=['POST'])
    def rafraichir(self):
        conducteurs = modeles.Conducteur.query.all()
        geojson = [
            json.loads(
                db.session.scalar(
                    ST_AsGeoJSON(
                        conducteur.position
                    )
                )
            )
            for conducteur in conducteurs
        ]
        return jsonify({
            'taxis': geojson,
            #'conducteurs': conducteurs
        })
 
       
admin.add_view(
    VueCarte(
        name='Carte',
        url='carte'
    )
)

