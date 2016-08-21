# install.packages("jsonlite")
# install.packages("sqldf")
# install.packages("gdata")
#install.packages("dplyr")
library(sqldf)
library(jsonlite)
library(dplyr)


#Récupération des données brutes via API

#Adresse api

con <- "https://fb3d8126.ngrok.io"

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
#Forfaits
Forfaits <- as.data.frame(fromJSON(paste(con,"/api/forfaits",sep =""))[1])
names(Forfaits) <- sub("^data.", "", names(Forfaits))

#Jointure entre tables
convert_to_encoding <- 
  function(x, from_encoding = "UTF-8", to_encoding = "cp1250"){
    
    # names of columns are encoded in specified encoding
    my_names <- 
      iconv(names(x), from_encoding, to_encoding) 
    
    # if any column name is NA, leave the names
    # otherwise replace them with new names
    if(any(is.na(my_names))){
      names(x)
    } else {
      names(x) <- my_names
    }
    
    # get column classes
    x_char_columns <- sapply(x, class)
    # identify character columns
    x_cols <- names(x_char_columns[x_char_columns == "character"])
    
    # convert all string values in character columns to 
    # specified encoding
    x <- 
      x %>%
      mutate_each_(funs(iconv(., from_encoding, to_encoding)), 
                   x_cols)
    # return x
    return(x)
  }


##Nombre de taxi rattaché par stations

reqStatPos <-  
  "SELECT Adresses.lon as longitude, 
        Adresses.lat as latitude,
        Stations.nom,
        Stations.distance_entree as entree,
        Stations.distance_sortie as sortie
FROM    Adresses, Stations 
WHERE   Adresses.identifiant=Stations.adresse"

reqNbTaxiByStat <- 
  "SELECT count(telephone) as nb,station 
FROM Conducteurs 
GROUP BY station"


StatPos <- sqldf(reqStatPos)
#StatPos <- convert_to_encoding(StatPos, "UTF-8", "cp1250")
NbTaxiByStat <- sqldf(reqNbTaxiByStat)
#NbTaxiByStat <- convert_to_encoding(NbTaxiByStat, "UTF-8", "cp1250")

#Jointure données
TaxiByStat=merge(StatPos,NbTaxiByStat,by.x="nom",by.y="station",all.x=T)
TaxiByStat[is.na(TaxiByStat)]=0
TaxiByStat <- TaxiByStat[order(-TaxiByStat$nb),]

#Formatage pour leaflet
df_Stati <- sp::SpatialPointsDataFrame(
  cbind(
    TaxiByStat$longitude, # lat
    TaxiByStat$latitude  # lng
  ),
  data.frame(type = TaxiByStat$nom, 
             nb = TaxiByStat$nb,
             entree = TaxiByStat$entree,
             sortie = TaxiByStat$sortie
  )
)



##Visualisation clients

reqPosUtil = 
"SELECT Utilisateurs.*,
        Adresses.lon,
        Adresses.lat 
from    Utilisateurs,Adresses
Where   Adresses.identifiant = Utilisateurs.adresse"

PosUtil <- sqldf(reqPosUtil)

df_clien = cbind(PosUtil$lon,PosUtil$lat)


##Trajet des conducteurs dans la journée

#Trajet des conducteurs

reqTrajCondu = 
"SELECT Conducteurs.telephone,
        Conducteurs.nom,
        Positions.lat,
        Positions.lon,
        Positions.moment
from    Conducteurs,Positions
Where   Conducteurs.telephone=Positions.conducteur"

TrajCondu <- sqldf(reqTrajCondu)




df_Traj <- sp::SpatialPointsDataFrame(
  cbind(
    TrajCondu$lon, # lat
    TrajCondu$lat  # lng
  ),
  data.frame(time = TrajCondu$moment,nom =TrajCondu$nom
  )
)


#Courses
reqCourses= 
"SELECT Courses.numero,
        Conducteurs.nom as condu,
        Utilisateurs.nom as utili,
        Etapes.lon,
        Etapes.lat,
        moment
from    Etapes,
        Courses,
        Conducteurs,
        Utilisateurs
Where   Courses.numero=Etapes.course
and     Courses.utilisateur = Utilisateurs.telephone
and     Courses.conducteur = Conducteurs.telephone"

trajCourses <- sqldf(reqCourses)

df_trajCourses <- sp::SpatialPointsDataFrame(
  cbind(
    trajCourses$lon,
    trajCourses$lat
  ),
  data.frame(num = as.factor(trajCourses$numero),
             time = trajCourses$moment,
             condu = trajCourses$condu,
             utili = trajCourses$utili
  )
)


