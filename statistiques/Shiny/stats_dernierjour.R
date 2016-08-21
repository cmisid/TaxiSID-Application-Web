library(stringr)
library(ggplot2)
library(plotly) # graphiques
library(sqldf)
library(jsonlite)
library(dplyr)
library(shiny)
library(magrittr)
library(RPostgreSQL)
require("RPostgreSQL")

##############################################
######### Connexion base de données ##########
##############################################

#Connexion a l'API

con <- "http://20528601.ngrok.io"
detach("package:RPostgreSQL", unload=TRUE)

#Connexion a postgres

# drv <- dbDriver("PostgreSQL")
# # creates a connection to the postgres database
# # note that "con" will be used later in each connection to the database
# con <- dbConnect(drv, dbname = "taxisid",
#                  host = "localhost", port = 5433,
#                  user = "postgres", password = "houdini")
# 

#Récupération des données brutes via API

#Conducteurs
Conducteurs <- as.data.frame(fromJSON(paste(con,"/api/conducteurs",sep =""))[1])
names(Conducteurs) <- sub("^data.", "", names(Conducteurs))
#Utilisateurs
Utilisateurs <- as.data.frame(fromJSON(paste(con,"/api/utilisateurs",sep =""))[1])
names(Utilisateurs) <- sub("^data.", "", names(Utilisateurs))
#Adresses
Adresses <- as.data.frame(fromJSON(paste(con,"/api/adresses",sep =""))[1])
names(Adresses) <- sub("^data.", "", names(Adresses))
#Stations
Stations <- as.data.frame(fromJSON(paste(con,"/api/stations",sep =""))[1])
names(Stations) <- sub("^data.", "", names(Stations))
#Vehicules
Vehicules <- as.data.frame(fromJSON(paste(con,"/api/vehicules",sep =""))[1])
names(Vehicules) <- sub("^data.", "", names(Vehicules))
#Courses
Courses <- as.data.frame(fromJSON(paste(con,"/api/courses",sep =""))[1])
names(Courses) <- sub("^data.", "", names(Courses))
#Factures
Factures <- as.data.frame(fromJSON(paste(con,"/api/factures",sep =""))[1])
names(Factures) <- sub("^data.", "", names(Factures))
#Positions
Positions <- as.data.frame(fromJSON(paste(con,"/api/positions",sep =""))[1])
names(Positions) <- sub("^data.", "", names(Positions))
#Etapes
Etapes <- as.data.frame(fromJSON(paste(con,"/api/etapes",sep =""))[1])
names(Etapes) <- sub("^data.", "", names(Etapes))
#Propositions
Propositions <- as.data.frame(fromJSON(paste(con,"/api/propositions",sep =""))[1])
names(Propositions) <- sub("^data.", "", names(Propositions))

# Set plotly API's credentials
Sys.setenv("plotly_username"="Axel-BELLEC")
Sys.setenv("plotly_api_key"="v0bd613wd3")


# distance = R*acos(cos(a)*cos(b)*cos(c-d)+sin(a)*sin(b))
# 
# avec R le rayon de la terre (en metre pour obtenir un résultat en metre)
# a = latitude du point A (en radians)
# b = latitude du point B (en radians)
# c = longitude du point A (en radians)
# d = longitude du point B (en radians)

###########################################
############### CA Conducteurs#############
###########################################
#CA par conducteur par jour

CAConductjour <-sqldf("SELECT montant as CA,Nom, fin as Date from Factures,Courses,Conducteurs 
                            where Factures.course=Courses.numero AND Courses.conducteur=Conducteurs.telephone group by Date, CA,Nom")

CAConductjour[,3]=str_sub(CAConductjour[,3],1,10)

#CA par conducteur par mois
CAConductmois=CAConductjour
CAConductmois[,3]=str_sub(CAConductjour[,3],1,7)
CAConductmois=aggregate(CAConductmois$CA,list(CAConductmois$Date,CAConductmois$nom),sum)
colnames(CAConductmois)=c("Date","Nom","CA")

#CA par conducteur par annee
CAConductannee=CAConductjour
CAConductannee[,3]=str_sub(CAConductjour[,3],1,4)
CAConductannee=aggregate(CAConductannee$CA,list(CAConductannee$Date,CAConductannee$nom),sum)
colnames(CAConductannee)=c("Date","Nom","CA")

#CA par conducteur par semaine
CAConductsem=CAConductjour
CAConductsem$Date=format(as.Date(CAConductjour$Date), "%U-%Y")
CAConductsem=aggregate(CAConductsem$CA,list(CAConductsem$Date,CAConductsem$nom),sum)
colnames(CAConductsem)=c("Date","Nom","CA")

#####################################
### Nb de conducteurs par station ###
#####################################

ConductByStation <- sqldf("select count(telephone),station from Conducteurs group by station")

#####################################
############# CA Total ##############
#####################################

#CA par jour
CAjour <- sqldf("SELECT sum(montant) as CA,(fin) as Date from Factures,Courses,Conducteurs 
                     where Factures.course=Courses.numero AND Courses.conducteur=Conducteurs.telephone group by Date")
CAjour[,2]=str_sub(CAjour[,2],1,10)
CAjour$Date=as.Date(CAjour$Date)
CAjour=aggregate(CA~Date,CAjour,sum)
#plot(CAjour$Date,CAjour$CA,ylab="CA journalier",xlab="Date",main="CA par jour",type="o")

#CA par semaine
CAsemaine = CAjour
CAsemaine$Date=format(as.Date(CAjour$Date), "%U-%Y")
CAsemaine=aggregate(CAsemaine$CA,list(CAsemaine$Date),sum)
colnames(CAsemaine)=c("Semaine","CA")

#CA par mois
CAmois <- sqldf("SELECT montant as CA,(fin) as Date from Factures,Courses,Conducteurs 
                     where Factures.course=Courses.numero AND Courses.conducteur=Conducteurs.telephone")

CAmois[,2]=str_sub(CAmois[,2],1,7)
CAmois=aggregate(CAmois$CA,list(CAmois$Date),sum)
colnames(CAmois)=c("Date","CA")

#CA par annee
CAannee <- sqldf("SELECT montant as CA,(fin) as Date from Factures,Courses,Conducteurs 
                      where Factures.course=Courses.numero AND Courses.conducteur=Conducteurs.telephone")

CAannee[,2]=str_sub(CAannee[,2],1,4)
CAannee=aggregate(CAannee$CA,list(CAannee$Date),sum)
colnames(CAannee)=c("Annee","CA")

##################################
###### CA moyen par courses ######
##################################

#CA moyen par jour
CAMoyen=merge(Nbcoursesjour,CAjour,by.x="Date",by.y="Date",all.x=T)
CAMoyen$Date=as.Date(CAMoyen$Date)
CAMoyen[,3]=CAMoyen$CA/CAMoyen$Nbcourses
#plot(CAMoyen$Date,(CAMoyen$CA/CAMoyen$Nbcourses),xlab="Date",ylab="CA moyen par jour",main="CA moyen par jour",type="l")

################################
######### Nbcourses ############
################################

#Nombre de courses par jour
Nbcoursesjour <- sqldf("SELECT count(telephone) as Nbcourses, fin as Date from Factures,Courses,Conducteurs 
                            where Factures.course=Courses.numero AND Courses.conducteur=Conducteurs.telephone group by Date")

Nbcoursesjour[,2]=str_sub(Nbcoursesjour[,2],1,10)
Nbcoursesjour$Date=as.Date(Nbcoursesjour$Date)
Nbcoursesjour=aggregate(Nbcoursesjour$Nbcourses,list(Nbcoursesjour$Date),sum)
colnames(Nbcoursesjour)=c("Date","Nbcourses")

#plot(Nbcourses$date,Nbcourses$nbcourses,ylab="Nombre de courses",xlab="Date",main="Nombre de courses par jour",type="o")

#Nombre de courses par mois
Nbcoursesmois=Nbcoursesjour
Nbcoursesmois[,1]=str_sub(Nbcoursesmois[,1],1,7)
Nbcoursesmois=aggregate(Nbcoursesmois$Nbcourses,list(Nbcoursesmois$Date),sum)
colnames(Nbcoursesmois)=c("Date","Nbcourses")

#Nombre de courses par annee
Nbcoursesannee=Nbcoursesjour
Nbcoursesannee[,1]=str_sub(Nbcoursesannee[,1],1,4)
Nbcoursesannee=aggregate(Nbcoursesannee$Nbcourses,list(Nbcoursesannee$Date),sum)
colnames(Nbcoursesannee)=c("Annee","Nbcourses")

#Nombre de courses par semaine
Nbcoursessem=Nbcoursesjour
Nbcoursessem$Date=format(as.Date(Nbcoursesjour$Date), "%U-%Y")
Nbcoursessem=aggregate(Nbcoursessem$Nbcourses,list(Nbcoursessem$Date),sum)
colnames(Nbcoursessem)=c("Semaine","Nbcourses")


##########################################
######### Nbcourses par condu ############
##########################################

#Nombre de courses par conducteurs et par jour
Nbcoursescondujour <- sqldf("SELECT count(telephone) as Nbcourses, fin as Date, nom from Factures,Courses,Conducteurs 
                                 where Factures.course=Courses.numero AND Courses.conducteur=Conducteurs.telephone group by Date,nom")


Nbcoursescondujour[,2]=str_sub(Nbcoursescondujour[,2],1,10)
Nbcoursescondujour$Date=as.Date(Nbcoursescondujour$Date)
Nbcoursescondujour=aggregate(Nbcoursescondujour$Nbcourses,list(Nbcoursescondujour$Date,Nbcoursescondujour$nom),sum)
colnames(Nbcoursescondujour)=c("Date","Nom","Nbcourses")

#plot(Nbcourses$date,Nbcourses$nbcourses,ylab="Nombre de courses",xlab="Date",main="Nombre de courses par jour",type="o")

#Nombre de courses par conducteurs et par mois
Nbcoursescondumois=Nbcoursescondujour
Nbcoursescondumois[,1]=str_sub(Nbcoursescondumois[,1],1,7)
Nbcoursescondumois=aggregate(Nbcoursescondumois$Nbcourses,list(Nbcoursescondumois$Date,Nbcoursescondumois$Nom),sum)
colnames(Nbcoursescondumois)=c("Date","Nom","Nbcourses")

#Nombre de courses par conducteurs et par annee
Nbcoursesconduannee=Nbcoursescondujour
Nbcoursesconduannee[,1]=str_sub(Nbcoursesconduannee[,1],1,4)
Nbcoursesconduannee=aggregate(Nbcoursesconduannee$Nbcourses,list(Nbcoursesconduannee$Date,Nbcoursesconduannee$Nom),sum)
colnames(Nbcoursesconduannee)=c("Annee","Nom","Nbcourses")

#Nombre de courses par conducteurs et par semaine
Nbcoursescondusem=Nbcoursescondujour
Nbcoursescondusem$Date=format(as.Date(Nbcoursescondujour$Date), "%U-%Y")
Nbcoursescondusem=aggregate(Nbcoursescondusem$Nbcourses,list(Nbcoursescondusem$Date,Nbcoursescondusem$Nom),sum)
colnames(Nbcoursescondusem)=c("Semaine","Nom","Nbcourses")

###########################################
###############Utilisateurs################
###########################################

#Depense par utilisateur par jour
depensejour <- sqldf("SELECT montant as Depense,utilisateurs.nom, fin as Date from Factures,Courses,Utilisateurs 
                         where Factures.course=Courses.numero AND Courses.utilisateur=Utilisateurs.telephone")
depensejour[,3]=str_sub(depensejour[,3],1,10)
depensejour=aggregate(depensejour$Depense,list(depensejour$Date,depensejour$nom),sum)
colnames(depensejour)=c("Date","Nom","Depense")

#Depense par utilisateur par mois
depensemois=depensejour
depensemois[,1]=str_sub(depensemois[,1],1,7)
depensemois=aggregate(depensemois$Depense,list(depensemois$Date,depensemois$Nom),sum)
colnames(depensemois)=c("Date","Nom","Depense")

#Depense par utilisateur par annee
depenseannee=depensemois
depenseannee[,3]=str_sub(depenseannee[,3],1,4)
#depenseannee=aggregate(depenseannee$Depense,list(depenseannee$Date,depenseannee$Nom),sum)

#Depense par utilisateur par semaine
depensesem=depensejour
depensesem$Date=format(as.Date(depensesem$Date), "%U-%Y")
depensesem=aggregate(depensesem$Depense,list(depensesem$Nom,depensesem$Date),sum)
colnames(depensesem)=c("Nom","Semaine","Depense")


#########################################
################ Trajet #################
#########################################

distance <- sqldf("SELECT distance_estimee,nom,fin as date from Courses,Conducteurs 
                       where Courses.conducteur=Conducteurs.telephone")

#Distance parcouru par condyucteur et par jour
distancejour=distance
distancejour[,3]=str_sub(distance[,3],1,10)
distancejour=aggregate(distancejour$distance_estimee,list(distancejour$nom,distancejour$date),sum)
colnames(distancejour)=c("Nom","Date","NbKm")

#Distance parcouru par condyucteur et par mois
distancemois=distancejour
distancemois[,2]=str_sub(distancemois[,2],1,7)

#Distance parcouru par condyucteur et par annee
distanceannee=distancejour
distanceannee[,2]=str_sub(distanceannee[,2],1,4)

#Distance parcouru par condyucteur et par semaine
distancesem=distancejour
distancesem$Date=format(as.Date(distancesem$Date), "%U-%Y")
distancesem=aggregate(distancesem$NbKm,list(distancesem$Nom,distancesem$Date),sum)
colnames(distancesem)=c("Nom","Semaine","NbKm")

#########################################
############### Plot ####################
#########################################

#Graph CA par jour
CAj <- ggplot(data=CAjour, aes(x=Date, y=CA, shape="CA"))
CAj <- CAj + geom_point(size=4,col="blue")
CAj <- CAj + ggtitle("CA par jour")
CAj <- CAj + geom_line(size=2)
print(CAj)
ggplotly(CAj)

#Graph CA par semaine
CAh <- ggplot(data=CAsemaine, aes(x=Semaine, y=CA, shape="CA"))
CAh <- CAh + geom_point(size=4,col="blue")
CAh <- CAh + ggtitle("CA par semaine")
CAh <- CAh + geom_line(size=2)
print(CAh)
ggplotly(CAh)

#Graph CA par mois
CAm <- ggplot(data=CAmois, aes(x=Date, y=CA, shape="CA"))
CAm <- CAm + geom_point(size=4,col="blue")
CAm <- CAm + ggtitle("CA par semaine")
CAm <- CAm + geom_line(size=2)
print(CAm)
ggplotly(CAm)

#Graph CA par annee
CAa <- ggplot(data=CAannee, aes(x=Annee, y=CA, shape="CA"))
CAa <- CAa + geom_point(size=4,col="blue")
CAa <- CAa + ggtitle("CA par semaine")
CAa <- CAa + geom_line(size=2)
print(CAa)
ggplotly(CAa)


#Graph nombre de courses
NBc <- ggplot(data=Nbcoursesjour, aes(x=Date, y=Nbcourses, colour="nbcourses",shape="nbcourses"))
NBc <- NBc + geom_point(size=4,col="blue")
NBc <- NBc + ggtitle("CA par jour")
NBc <- NBc + geom_line(size=2)
print(NBc)
ggplotly(NBc)

# Graph CA moyen par course
CAmoy <- ggplot(data=CAMoyen, aes(x=Date, y=CA, colour="ca",shape="ca"))
CAmoy <- CAmoy + geom_point(size=4,col="blue")
CAmoy <- CAmoy + ggtitle("CA par jour")
CAmoy <- CAmoy + geom_line(size=2)
CAmoy <- CAmoy + theme(legend.position="top")
print(CAmoy)
ggplotly(CAmoy)



