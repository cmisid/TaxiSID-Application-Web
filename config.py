# Clé secrète pour générer des tokens
SECRET_KEY = 'houdini'
# Identifiants administrateurs
ADMIN_CREDENTIALS = ('admin', 'pa$$')
# DEBUG doit être False en production par souçi de sécurité
DEBUG = True
# Détail de la connexion à PostgreSQL
bd_utilisateur = 'postgres'
bd_mot_de_passe = 'houdini'
bd_port = '5433'
bd_nom = 'taxisid'
SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@localhost:{2}/{3}'.format(
    bd_utilisateur,
    bd_mot_de_passe,
    bd_port,
    bd_nom
)
SQLALCHEMY_TRACK_MODIFICATIONS = True
# Configuration du serveur gmail pour envoyer des mails
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'noreply.taxisid'
MAIL_PASSWORD = '464PK2wnSY774_K'
ADMINS = ['noreply.taxisid@gmail.com', 'contact.taxisid@gmail.com']
# Nombre de fois qu'un mot de passe est hashé
BCRYPT_LOG_ROUNDS = 12
# Identifiants Mapbox pour l'interface administrateur
MAPBOX_MAP_ID = 'mapbox.streets'
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoibGVtYXgiLCJhIjoidnNDV1kzNCJ9.iH26jLhEuimYd6vLOO6v1g'
