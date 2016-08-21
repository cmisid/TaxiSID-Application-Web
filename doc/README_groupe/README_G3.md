# Groupe 3 - Formulaire et compte utilisateur

*Documentation du groupe G3 chargé d'établir un formulaire de réservation de taxi, et de s'occuper de la gestion de comptes utilisateurs.*


# LA GESTION DU MODÈLE/VUE/CONTRÔLEUR DE `Flask`

Le **modèle** contient les données manipulées par l’application. Il assure la gestion de ces données et garantit leur intégrité. Dans le cas typique d'une base de données, c'est le modèle qui est responsable des données, il les récupères, les convertis et les enregistre.

La **vue** fait l’interface avec l’utilisateur. Elle représente une présentation des données venant du modèle.

Le **contrôleur** est chargé de la synchronisation du modèle et de la vue. Il gère les requêtes de l’utilisateur et est responsable de retourner une réponse avec l’aide mutuelle de la vue et du modèle.

# GESTION DE COMPTES UTILISATEUR

Chaque utilisateur à la possibilité de se créer un compte utilisateur, via un formulaire d'enregistrement. Une fois le formulaire validé, il reçoit un mail de confirmation automatique. Cette gestion se fait principalement dans le fichier `/app/formulaires/utilisateurs.py`. Dans la BD les tables sollicitées sont les tables Utilisateurs et Adresses. 

## ENREGISTREMENT

Chaque personne qui le souhaite peut s’enregistrer sur le site en créant un compte. Nous nous trouvons sur la page d’enregistrement. On demande à l’utilisateur de saisir des informations personnelles (nom/prénom, coordonnées), au travers d’un formulaire. Ces informations vont nous servir à créer le compte de l’utilisateur. 
Cette gestion se fait principalement dans le fichier `/app/formulaires/utilisateurs.py` à l’aide de la classe *enregistrement*. Dans la BD la table sollicitée est la table Utilisateurs.
L’utilisateur va ensuite recevoir un mail dans lequel il va pouvoir confirmer son adresse mail et il sera redirigé vers la page d’accueil.

## CONNEXION

Une fois la personne enregistrée, elle à la possibilité de se connecter sur le site.
Elle se trouve sur la page de connexion, et après avoir rempli les informations nécessaires à son authentification (adresse e-mail et mot de passe) elle est redirigée sur la page d’accueil où elle peut effectuer une réservation. Ensuite, elle n’a pas à remplir tous les champs car ceux déjà définis lors de son inscription sont déjà récupérés comme le nom/prénom.
Elle peut, sur la page connexion, signaler qu’elle a oublié sont mot de passe. On lui envoie donc un mail avec un lien où elle pourra en redéfinir un nouveau.
Cette gestion se fait principalement dans le fichier `/app/formulaires/utilisateurs.py` à l’aide de la classe *connexion*. Dans la BD la table sollicitée est la table Utilisateurs.



# FORMULAIRE DE RÉSERVATION

Chaque personne peut réserver un Taxi en remplissant le formulaire de réservation présent sur la page d'accueil. 
Si la personne ne possède pas de compte, son numero de téléphone suffira pour lui octroyer une course, l'application se déplace ainsi dans les différentes tables pour lui attribuer un conducteur.
Si la personne possède un compte et est connectée, c’est un formulaire adapté qui lui sera proposé car on connait déjà plusieurs informations sur cette personne.
Hormis les informations complémentaires, tous les champs doivent obligatoirement être complètés pour effectuer une réservation.
Cette gestion se fait principalement dans le fichier `/app/formulaires/reservation.py`.
On se trouve sur la route index dans le fichier `/app/vues/course.py`
Une fois les champs complètés correctement, l’utilisateur est redirigé vers la page devis, où on lui affichera un devis prévisionnel. Un module de contrôle des champs entrés dans le formulaire permet d'effectuer des vérifications complémentaires :
- adresse géolocalisable
- numéro de téléphone bien constitué de 10 chiffres
- adresse email au bon format

## DEVIS PRÉVISIONNEL
Pour chaque demande de réservation effectuée par un utilisateur nous lui affichons un devis prévisionnel où sont explicités les différentes composantes du prix (distance, nombre de bagages, nombre d’animaux, proximité à la gare ou à l'aéroport).
Après avoir regardé le devis, la personne présente sur le site peut soit accepter la réservation de la course, soit la décliner.
Si elle accepte la course, on lui envoie un mail où elle pourra visualiser un récapitulatif du devis prévisionnel. Afin de confirmer la course, on entre les informations du formulaires dans la base de donnée afin de pouvoir par la suite lui attribuer un conducteur puis on redirige la personne sur la page d’accueil.
Si elle la décline, on redirige la personne sur le formulaire de réservation.
On se trouve sur la route `index` dans le fichier `/app/vues/course.py`
Dans la BD les tables sollicitées sont les tables Utilisateurs, Courses, Adresses et Factures.

