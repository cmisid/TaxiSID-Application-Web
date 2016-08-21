from flask import Flask

app = Flask(__name__)

# Générer l'application avec les options du fichier config.py
app.config.from_object('config')

# Se connecter à la base de données
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Mettre en place le serveur email
from flask.ext.mail import Mail
mail = Mail(app)

# Mettre en place l'outil pour générer des clés secrètes
from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Ajouter une interface administrateur
from flask_admin import Admin
admin = Admin(app, 'Administration', base_template='admin.html',
			  template_mode='bootstrap3')

# Mobiliser l'application
from flask.ext.mobility import Mobility
mobile = Mobility(app)

# Importer les vues classiques
from app.vues import (
	principal,
	utilisateur,
	erreur,
	conducteur,
	course
)

app.register_blueprint(utilisateur.utilisateurbp)
app.register_blueprint(conducteur.conducteurbp)

# Importer les vues de l'API
from app.vues.api import (
	adresses,
	base,
	conducteurs,
	stations,
	messages
)

app.register_blueprint(adresses.apiadressebp)
app.register_blueprint(base.apibp)
app.register_blueprint(conducteurs.apiconducteurbp)
app.register_blueprint(messages.apimessagebp)
app.register_blueprint(stations.apistationbp)

# Importer les vues administrateurs
from app.vues.admin import (
	courses,
	utilisateurs,
	conducteurs,
	entreprises,
	vehicules,
	stations,
	paiements,
	adresses,
	statistiques,
	carte
)

# Mettre en place la gestion de compte utilisateur
from flask.ext.login import LoginManager
from app.modeles import Utilisateur

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'utilisateurbp.connexion'


@login_manager.user_loader
def load_user(telephone):
    return Utilisateur.query.filter(Utilisateur.telephone == telephone).first()

# Langue française
from flask import request
from flask_babelex import Babel

babel = Babel(app)

@babel.localeselector
def get_locale():
    return 'fr'
