# TaxiSID

![Logo](app/static/img/taxisid.jpg)

##Dossier Production

- ``Dossier app`` : contient tous les fichiers relatifs au fonctionnement de l'application.
- ``Dossier doc`` : contient la documentation du projet, à propos de la base de données, du suivi de production, de l'architecture de l'application ou encore le rôle de chacun des groupes.
- ``Dossier setup`` : contient des fichiers d'installation au sujet du déploiement d'un serveur (ce dossier est non utilisé à ce jour).
- ``Dossier tests`` : contient tous les fichiers de tests créés par les groupes de projet, en collaboration avec le groupe qualité.
- ``Fichiers racines`` :
  * ``config.py, creation.py, insertions.py, suppression.py`` : fichiers relatifs à la base de données.
  * ``requirements.txt`` : contient tous les packages nécessaires à installer.
  * ``run.py`` : fichier permettant d'exécuter l'application.
  * ``test.bat, test.sh`` : exécutable permettant d'exécuter tous les fichiers évoqués précédemment (fichiers base de données, requirements.txt et run.py). Le fichier .bat est destiné aux utilisateurs de Windows et le fichier .sh aux utilisateurs de Mac/Linux.

## Architecture

- [Visuel](doc/architecture.png)

## Utilisation

Il faut d'abord s'assurer que les valeurs dans ``config.py`` soient cohérentes, notamment pour ce qui est des détails de connexion à la base de données.

- ``bd_utilisateur``, configuré lors de l'installation de PostgreSQL.
- ``bd_mot_de_passe``, configuré lors de l'installation de PostgreSQL.
- ``bd_port``, configuré lors de l'installation de PostgreSQL (5432 par défaut).
- ``bd_nom``, on préfèrera le nom ``taxisid`` pour bien s'y retrouver dans pgAdmin.

Afin de pouvoir supprimer l'ancienne base de données, créer la nouvelle, la remplir, tester le code et enfin exécuter l'application, il suffit de lancer les commandes suivantes:

```sh
# On installe les packages nécessaire
pip install -r requirements.txt
# On supprime l'ancienne BD
python suppression.py
# On crée la BD
python creation.py
# On remplit la BD
python insertions.py
# On lance les tests
nosetests
# On lance l'application
python run.py
```

Ces opérations sont automatisées grâce aux scripts ``test.sh`` sur une machine UNIX et ``test.bat`` sur Windows.

Si la commande de test ne s'exécute pas correctement, il suffit de taper dans la console :
  * Pour mac et linux : ``export PYTHONPATH=${PYTHONPATH}:/[chemin jusqu'à production]/``
  * Pour windows : ``set PYTHONPATH=%PYTHONPATH%;C:\My_python_lib``

Par défaut l'application est accessible à l'URL ``localhost:5000`` dans le navigateur.

#### Partage du localhost

Il faut utiliser l'utilitaire ``ngrok``. Celui-ci est téléchargeable [ici](https://ngrok.com/download). Commencez pas dézipper le téléchargement et à inclure le binaire qui s'appelle ``ngrok`` à la racine. Tapez ensuite ``python run.py`` dans une console. Puis ouvrez une nouvelle console puis tapez ``./ngrok http 5000``, ``ngrok`` vous informe alors de l'URL à laquelle le localhost est disponible.

Ceci est extrêmement pratique pour, par exemple, développer une application portable qui va accéder à la base de données via une API.

#### Déploiement sur un serveur

Se référer au dossier ``setup/``.

## Installation de packages

Le fichier ``requirements.txt`` liste toutes les librairies Python à installer, cependant certaines peuvent poser problème avec l'utilitaire d'installation de base (``pip``).

#### Installer shapely

##### Sur Linux

```sh
sudo apt-get build-dep python-shapely

##### Sur Windows
  
Téléchargez la dernière version de la librairie ``shapely`` sur [ce site](http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely) puis mettez la dans le dossier de votre projet.

```sh
# Se placer dans le dossier où se trouve le fichier
pip install nomdufichier.whl
```

##### Sur MacOS

```sh
# Installer Geos
brew install geos
# Installer Shapely
brew install python-shapely
pip install shapely
```

Si vous n'avez pas ``brew`` d'installé, vous pouvez le faire avec la commande suivante:

```sh
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

#### Installer psycopg2

##### Sur Windows et Linux

Téléchargez la librairie ``psycopg2`` [ici](http://www.lfd.uci.edu/~gohlke/pythonlibs/#psycopg) puis le mettre à la racine du projet.

```sh
# Installer psycopg2
pip install psycopg2
```

Attention vous pouvez avoir une erreur psycopg2 si vous n'avez pas mis votre mot de passe postgre dans le fichier config.py, voir la partie utilisation ci-dessus.

##### Sur MacOS

Il faut d'abord indiquer le chemin vers l'exécutable de PostgreSQL, installer ``psycopg2`` via ``pip`` et enfin changer la librairie /usr/lib/libpq.5.dylib car elle est trop vieille avec les commandes suivantes:

```sh
export PATH="/Library/PostgreSQL/9.4.5/bin:$PATH"
anaconda/bin/pip install psycopg2
sudo mv /usr/lib/libpq.5.dylib /usr/lib/libpq.5.dylib.old
sudo ln -s /Library/PostgreSQL/9.4.5/lib/libpq.5.dylib /usr/lib
```

Si vous avez OS X El Capitan, que les commandes précédentes ne fonctionnent pas ou que vous avez un message d'erreur en important ``psycopg2`` dans Python, veuillez suivre les consignes suivantes:

```sh
anaconda/bin/pip install psycopg2
sudo chown -R $(whoami):admin /usr/local
sudo ln -s /Library/PostgreSQL/9.4.5/lib/libssl.1.0.0.dylib /usr/local/lib/
sudo ln -s /Library/PostgreSQL/9.4.5/lib/libcrypto.1.0.0.dylib /usr/local/lib/
```

Puis installez psycopg2:

```sh
pip install psycopg2
```

## API

L'API renvoit des données au format JSON, l'URL d'accès de celle-ci est ``~/api/``. Les tables de la base de données sont directement accessibles via l'API, il suffit d'accéder à ``~/api/<table>``. Les tables sont automatiquement traitées pour ne pas afficher les attributs commencant avec un ``_`` (par exemple un mot de passe). De plus, l'API transforme les objets PostGIS en données longitunidales.


## Motivation

Ce projet a été proposé par la société [CapitoleTaxi](http://www.capitole-taxi.com/reserver-un-taxi-toulouse-midi-pyrenees-50.html). Notre équipe a pour but de créer une application web et mobile. Celle-ci doit permettre à des utilisateurs de réserver un taxi et doit permettre aux taxis d'accepter ou non les courses qu'on leur propose. Une demande de course doit être proposé aux taxis les plus proches de l'adresse de départ de l'utilisateur.


## Contributeurs

Ce projet est réalisé par tous les élèves de [la formation CMI SID de Toulouse](https://cmisid.univ-tlse3.fr/) de l'Université Paul Sabatier, avec l'aide de certains de leurs professeurs.
