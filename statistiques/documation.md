#Documentation du groupe 8 Statistiques
	
Le package R shiny permet de développer des applications web intéractives grâce au langage de programmation R. L’application que nous avons réalisée se présente comme un tableau de bord donnant des statistiques sous forme d’indicateurs, de graphiques ou encore de cartes, qui permettront à Capitole Taxi de mieux gérer son activité. L’objectif principal étant de mieux répartir les taxis en fonction des demandes par station (secteur).
	
##Import des données et déploiement
Nous avons récupéré les données via l’API de l’application globale TaxiSid. Pour l’instant, cette dernière ne se lance qu’en locale. C'est-à-dire que nous lançons le site via nos ordinateurs et il n’est qu’accessible à l’adresse « localhost :5000 » après avoir lancé les fichiers adéquats. En utilisant l’outil « ngrok », on peut partager le localhost. C’est comme cela que l'on peut accéder à l’API. Vous pouvez voir que dans le fichier  « extractAPI.R » il y a une variable « con » qui prend la valeur d’un site. Ce dernier est en fait l’adresse grace à laquelle on peut accéder à notre localhost via ngrok.

Par conséquent, pour pouvoir lancer l’application, il faut exécuter toutes ces étapes, et remplacer l’adresse dans la variable « con » par votre adresse « ngrok ».
Une fois que vous avez fait cela et que l’application RShiny fonctionne en locale, vous pouvez la déployer sur le site shinyapps.io grâce à certaines manipulations que vous pouvez voir dans « déploiement.R »(Il faut se créer un compte au préalable). Une fois ce déploiement fait, tout le monde peut accéder à votre application via ce site.

Le gros problème est que pour l’instant l’application TaxiSid n’est pas hébergée sur un serveur et ne possède pas d’adresse internet fixe. De ce fait, il n’y a pas non plus d’adresse fixe pour l’API, donc une fois que vous coupez la connexion au site via « ngrok », l’application ne se lance plus en locale, ni sur « shinyapps.io » et par conséquent, elle ne s’affiche plus sur l’application globale TaxiSid.

Une fois que l’application aura une adresse fixe, ce problème sera résolu.

##Description de l’application
	Pour  l’instant l’application est composée de 5 onglets eux-mêmes comportant différents indicateurs :
* Conducteurs
    * Une carte affichant les trajets d’un conducteur sélectionné. 
* Client
    * Carte donnant la position des clients.
* Stations
    * Carte affichant les stations avec leurs rayons d’actions accompagnées d’un code couleur en fonction des taxis rattachés aux stations.
* Courses
    * Carte affichant les trajets des courses (sélectionnables en fonction du conducteur, puis du numéro de la course).
* Factures
    * Graphiques sur le chiffre d’affaire ou encore le nombre de courses.
	
	
##Utilisation
Comme on peut vite le remarquer, il y a des zones de sélections à gauche de l’application ainsi que dans l’onglet courses. Ces listes déroulantes sont réactives entre-elles. En choisissant la station « Balma » par exemple, seuls les conducteurs rattachés à cette station seront affichés. De la même façon, seules les courses du conducteur en question seront proposées.
 
 
##Idées pour la suite
Une des idées principales pour apporter plus de fonctionnalités à l’application, serait de rajouter des zones de sélections, pour choisir le jour, le mois, l’année par exemple. Cela permettrait à l’utilisateur d’avoir différentes échelles de précisions et ainsi moduler son analyse à sa guise.

Ensuite, des améliorations aux niveaux des cartes sont à apporter absolument. Par exemple, des statistiques par rapport aux utilisateurs réguliers pourraientt être affichées lorsqu’on clique dessus. Pour les stations, afficher le nombre de taxis par stations en fonction de leurs statuts (Disponible, en pause, occupé …).

Concernant les statistiques à intégrer à l’application, nous avons déjà réalisé beaucoup de graphiques en tout genre que nous n’avons pas eu le temps d’intégrer à l’application finale pour différentes raisons (Notamment un souci au moment du déploiement de l’application de shinyapps.io). Vous pouvez retrouver le code pour obtenir ces graphiques dans les différents fichiers mis à disposition. De plus, nous avons réfléchis à plusieurs idées intéressantes de statistiques inférentielles et de prédictions qu’il serait possible de réaliser avec un historique de données. Vous pouvez retrouver tout ce que nous avons déjà fait ainsi que les idées auxquelles nous avons pensé dans le fichier « JournalDeBord.md ».


