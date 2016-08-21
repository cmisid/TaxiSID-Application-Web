library(stringr)
library(ggplot2)
library(plotly) # graphiques
library(sqldf)

# Set plotly API's credentials
Sys.setenv("plotly_username"="Axel-BELLEC")
Sys.setenv("plotly_api_key"="v0bd613wd3")





#Creation graphique CA par jours
reqCAjour <- 
"SELECT sum(montant) as CA,(fin) as date 
from    Factures,Courses,Conducteurs 
where   Factures.course=Courses.numero AND Courses.conducteur=Conducteurs.telephone group by Date"


CAjour <- sqldf(reqCAjour)


CAjour[,2]=str_sub(CAjour[,2],1,10)
CAjour$date=as.Date(CAjour$date)
CAjour=aggregate(CA~date,CAjour,sum)


CAj <- ggplot(data=CAjour, aes(x=date, y=CA, shape="ca"))
CAj <- CAj + geom_point(size=1,col="blue")
CAj <- CAj + ggtitle("CA par jour")
CAj <- CAj + geom_line(size=0.25, col="green")


####Creation graphique nombre de courses par jours

#Récupération des données
ReqNbcourses <- 
"SELECT count(telephone) as nbcourses, 
        fin as date 
from    Factures,
        Courses,
        Conducteurs 
where   Factures.course=Courses.numero 
AND     Courses.conducteur=Conducteurs.telephone 
group by date"
Nbcourses <- sqldf(ReqNbcourses)

#Formatage
Nbcourses[,2]=str_sub(Nbcourses[,2],1,10)
Nbcourses$date=as.Date(Nbcourses$date)
Nbcourses=aggregate(nbcourses~date,Nbcourses,sum)

#Création du graphique
NBc <- ggplot(data=Nbcourses, aes(x=date, y=nbcourses, colour="nbcourses",shape="nbcourses"))
NBc <- NBc + geom_point(size=1,col="blue")
NBc <- NBc + ggtitle("Nb de courses par jour")
NBc <- NBc + geom_line(size=0.25, col="green") + theme(legend.position="bottom")


CAMoyen=merge(Nbcourses,CAjour,by.x="date",by.y="date",all.x=T)
CAMoyen$date=as.Date(CAMoyen$date)
CAMoyen[,3]=CAMoyen$CA/CAMoyen$nbcourses

CAmoy <- ggplot(data=CAMoyen, aes(x=date, y=CA, colour="ca",shape="ca"))
CAmoy <- CAmoy + geom_point(size=1,col="blue")
CAmoy <- CAmoy + ggtitle("CA moyen par jour")
CAmoy <- CAmoy + geom_line(size=0.25,col="green")




# reqTempsRepCondu= "SELECT avg(Propositions.reponse-Propositions.proposition) as tempsMoy, Conducteurs.nom
#               from Propositions, Conducteurs
#               where Conducteurs.telephone=Propositions.conducteur
#               GROUP BY Conducteurs.telephone
#               ORDER BY tempsMoy"
# 
# TempsRepCondu <- sqldf(reqTempsRepCondu)
# 
# sec <- c(TempsRepCondu$tempsmoy)
# TempsSec <- as.numeric(substring(sec,7,8))+as.numeric(substring(sec,4,5))*60+as.numeric(substring(sec,1,2))*3600
# 
# #server
# 
# TempsRepConduSec <- plot(as.factor(TempsRepCondu$nom),TempsSec, 
#                          main="Temps de réponse moyen par conducteur",
#                          xlab="Nom des conducteurs",
#                          ylab="Temps moyen des réponses en secondes")



