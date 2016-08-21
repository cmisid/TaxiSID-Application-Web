from app import db
from app import app
from app import modeles
from sqlalchemy import create_engine
import contextlib
import sqlalchemy.exc
import platform
import glob

# Création de la base de données

uri = app.config['SQLALCHEMY_DATABASE_URI'].split('/')
url = '/'.join(uri[:-1])
bd = uri[-1]

with contextlib.suppress(sqlalchemy.exc.ProgrammingError):
    with create_engine(url, isolation_level='AUTOCOMMIT').connect() as conn:
        conn.execute("CREATE DATABASE {} WITH encoding='utf-8'".format(bd))

print('Base de données créée.')

# Création des tables

db.session.execute("SET client_encoding='utf-8'")
db.session.execute('CREATE EXTENSION postgis')
db.session.commit()
db.create_all()

print('Tables créées.')

# Création des triggers

# Détection de l'OS
systeme = platform.system()
# Les slashs changent si on sur Windows
dossier = 'app\\triggers\*.sql' if systeme == 'Windows' else 'app/triggers/*.sql'

# Essayer d'exécuter tous les triggers dans le dossier qui les contient
for trigger in glob.glob(dossier):
	sql = open(trigger).read()
	try:
		db.session.execute(sql)
		db.session.commit()
		print('Trigger {} crée sans erreurs.'.format(trigger))
	except:
		print('Erreur sur le trigger {}.'.format(trigger))

print('Triggers crées.')
