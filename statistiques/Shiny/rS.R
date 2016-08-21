
#Nombre de propositions acceptées
NBAccepter <- "
            select distinct(C.telephone) as telephone, C.Nom, 0 as NBAccepter
              from Conducteurs C
            EXCEPT
            select distinct(C.telephone), C.Nom, 0
             from Conducteurs C, Propositions P
             where P.statut='Accepter'
             and P.conducteur=C.telephone
            group by C.telephone
            UNION
            select distinct(C.telephone) as telephone, C.Nom, count(P.statut) as NbAccepter
             from Conducteurs C, Propositions P
             where P.statut='Accepter'
            and P.conducteur=C.telephone
            group by C.telephone"
NBA <- sqldf(NBAccepter)
#Nombre de propositions refusées
NBRefuser <- "select distinct(C.telephone) as telephone, 0 as NBRefuser
              from Conducteurs C
            EXCEPT
              select distinct(C.telephone), 0
              from Conducteurs C, Propositions P
              where P.statut='Refuser'
              and P.conducteur=C.telephone
              group by C.telephone
            UNION
              select distinct(C.telephone) as telephone, count(P.statut) as NbRefuser
              from Conducteurs C, Propositions P
              where P.statut='Refuser'
              and P.conducteur=C.telephone
              group by C.telephone"
NBR <- sqldf(NBRefuser)

#Nombre de propositions totales
NBTotal <- "select distinct(C.telephone) as telephone, 0 as NBTotal
            from Conducteurs C
            EXCEPT
            select distinct(C.telephone), 0
            from Conducteurs C, Propositions P
           where P.conducteur=C.telephone
            group by C.telephone
            UNION
            select distinct(C.telephone) as telephone, count(P.statut) as TOTAL
            from Conducteurs C, Propositions P
            where P.conducteur=C.telephone
            group by C.telephone"
NBT <- sqldf(NBTotal)

# Tableaux du nombres de propositions acceptées, refusées et totales par conducteur
tabRA <- merge(NBA,NBR,by.x = "telephone", by.y = "telephone")
tabRAT <- merge(tabRA,NBT,by.x = "telephone", by.y = "telephone")

# Tableaux des taux de propostions 
tabRTaux <- (tabRAT$NBRefuser/tabRAT$NBTotal)*100
tabATaux <- (tabRAT$NBAccepter/tabRAT$NBTotal)*100
data <- cbind(tabRAT,tabATaux,tabRTaux)
data[is.na(data)] <- 0

# Graphique
x <- matrix(c(data$tabATaux,data$tabRTaux), nrow=length(data$C.Nom), ncol=2, dimnames = list(data$C.Nom,c("data$tabATaux","data$tabRTaux")))
x <- t(x)
# par(xpd = TRUE, mar=c(4.5,4,3,7))
