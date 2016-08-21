##########Statistiques jonathan

##Pourcentage des taxis affecter par stations
tabConduStat=table(Conducteurs$telephone,Conducteurs$station)
NbConduStat=apply(tabConduStat,2,sum)
tabPctConduStat = NbConduStat/sum(NbConduStat)*100 

##Type de paiement en fonction du montant
#Bonne idée mais faire des classes de prix je pense
#table(Factures$type_paiement,Factures$montant)# paiement selon le prix

G_TypePaiMontant <- ggplot(Factures, aes(x=course, y=montant, colour=type_paiement, shape=type_paiement))
G_TypePaiMontant <- G_TypePaiMontant + geom_point(size=1) 
G_TypePaiMontant <- G_TypePaiMontant + ggtitle("Mode de paiement selon le montant") 
G_TypePaiMontant <- G_TypePaiMontant +   geom_line(size=0.25)



# ggplotly(G_TypePaiMontant)

# 
# ##Différence entre estimation et montant
# #Idée : Retravailler histogramme, changer les classes
# 
# #Erreur sur le montant par rapport à estimation_1
# erreur1=Factures$montant-Factures$estimation_1
# mean(erreur1) # erreur moyenne
# # plot(erreur,ylab="erreur",xlab="numero",main="repartition des erreurs",type="o")
# # boxplot(erreur)
# hist(erreur1)
# 
# #Erreur sur le montant par rapport à estimation_2
# erreur2=Factures$montant-Factures$estimation_2
# mean(erreur2) # erreur moyenne
# # plot(erreur,ylab="erreur",xlab="numero",main="repartition des erreurs",type="o")
# # boxplot(erreur)
# hist(erreur2)
# 
# 
# # Table cours 
# # etude des commentaires
# # table(cours$commentaire)
# # numero des conducteurs dont le commentaire était moyen
# # Courses$conducteur[Courses$commentaire=="moyen"]
# 
# ## Idée : Sur commentaires, faire du texte mining ??
# 
# 
# #calcul de la différence entre la première et la deuxième estimation ( en valeur aboslu)
# DifEsti12=abs(Factures$estimation_1-Factures$estimation_2)
# # #coeff de variation pour
# CoefVar <- function( datum )
# {
#   # Fonction permettant de calculer le coefficient de variation
#   # Applicable seulement pour des données ayant un véritable zéro
#   # Calcul de l'écart type
#   EcartType <- sd(datum)
#   # Calcul de la moyenne
#   Moyenne <- mean(datum)
#   # Calcul du coefficient de variation
#   CV <- 100 * EcartType / Moyenne
#   # Retourne le résultat
#   return(CV)
# }
# 
# #regarder la dispersion des erreurs entre les deux estimations
# CVEsti <- CoefVar(datum=DifEsti12)
# 
# 
# 
# # représentation des différences entre les deux estimations
reqDifEstimHDep <- 
"Select SUBSTR(Courses.debut,12,2) as HDep,
        AVG(Factures.estimation_1 - Factures.estimation_2) as DifEstim
From    Courses, Factures
Where   Factures.course = Courses.numero
GROUP BY HDep
"
DifEstimHdep <- sqldf(reqDifEstimHDep)

G_DifEstimHDep <-ggplot(DifEstimHdep,aes(HDep,DifEstim,group = 1))  + 
  geom_point() + 
  geom_line(size = 0.25, col="green") +
  geom_hline(yintercept=c(sd(DifEstimHdep$DifEstim),-sd(DifEstimHdep$DifEstim)), color = "red", size = 0.1)+
  ggtitle("Différence des deux estimations par heure de départ")


# 
# ##Différence significative ? si oui différence en fonction de quoi ? Est ce que l'estimation est plus mauvaise en fonction de la destination ? Du trajet emprunté ? Quelle trajet ?
# #les différences suivent elles une densité de loi normale ? 
# g<-ggplot(fact, aes(x)) +
#   geom_histogram(aes(y = ..density..), color="black", fill=NA) +
#   geom_density(color="blue")
# g


