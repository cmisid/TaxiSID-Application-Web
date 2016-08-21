# Packages utilisés

library(shiny)
library(leaflet)
library(magrittr)
library(plotly)
library(ggplot2)
library(leaflet)


##Référence à d'autres fichiers pour les données utilisées
source("extractAPI.R")
source("statistiques.R")
#source("statjo.R")
#source("rS.R")



## Icones 
Ic_car<- makeIcon(
    iconUrl = "img/taxi.png",
    iconAnchorX = 10, iconAnchorY = 10,
    iconWidth = 25, iconHeight = 25
  )
Ic_personn<- makeIcon(
    iconUrl = "img/person.png",
    iconAnchorX = 10, iconAnchorY = 10,
    iconWidth = 25, iconHeight = 25
  )

##Palettes de couleurs

pal <- colorFactor(sort(heat.colors(4),decreasing = TRUE),
                   #Par rapport aux valeurs de nb
                   domain = df_Stati$nb)



# Définition du server Shiny
shinyServer(function(input, output) {
  
  #Variable reactive à la sélection du bouton
  Stations <- reactive({
    switch(input$selstation,
           "Toutes" = df_Stati,
           "Balma" = df_Stati[df_Stati$type == "Balma",],
           "Blagnac" = df_Stati[df_Stati$type == "Blagnac",],
           "Capitole" = df_Stati[df_Stati$type == "Capitole",],
           "Esquirol" = df_Stati[df_Stati$type == "Esquirol",],
           "Colomiers" = df_Stati[df_Stati$type == "Colomiers",],
           "FacultÃ© de pharmacie" = df_Stati[df_Stati$type == "Faculté de pharmacie",],
           "La Cepiere" = df_Stati[df_Stati$type == "La Cepiere",],
           "Minimes" = df_Stati[df_Stati$type == "Minimes",],
           "Ramonville" = df_Stati[df_Stati$type == "Ramonville",],
           "Rangueil" = df_Stati[df_Stati$type == "Rangueil",],
           "Tournefeuille" = df_Stati[df_Stati$type == "Tournefeuille",],
           "Aeroport" = df_Stati[df_Stati$type == "Aeroport",],
           "Arene" = df_Stati[df_Stati$type == "Arene",],
           "Astrium" = df_Stati[df_Stati$type == "Astrium",],
           "Barriere de Paris" = df_Stati[df_Stati$type == "Barriere de Paris",],
           "Basso Cambo" = df_Stati[df_Stati$type == "Basso Cambo",],
           "Borderouge" = df_Stati[df_Stati$type == "Borderouge",],
           "Carmes" = df_Stati[df_Stati$type == "Carmes",],
           "Cite Espace" = df_Stati[df_Stati$type == "Cite Espace",],
           "CNES" = df_Stati[df_Stati$type == "CNES",],
           "Compans" = df_Stati[df_Stati$type == "Compans",],
           "Fondere" = df_Stati[df_Stati$type == "Fondere",],
           "Gare" = df_Stati[df_Stati$type == "Gare",],
           "Hopital Rangueil" = df_Stati[df_Stati$type == "Hopital Rangueil",],
           "Jeanne dâ€™Arc" = df_Stati[df_Stati$type == "Jeanne d'Arc",],
           "La Cepiere" = df_Stati[df_Stati$type == "La Cepiere",],
           "La crabe" = df_Stati[df_Stati$type == "La crabe",],
           "Metro Argoulet" = df_Stati[df_Stati$type == "Metro Argoulet",],
           "Minimes" = df_Stati[df_Stati$type == "Minimes",],
           "Oncopole" = df_Stati[df_Stati$type == "Oncopole",],
           "Parc Expo" = df_Stati[df_Stati$type == "Parc Expo",],
           "Prison St Michel" = df_Stati[df_Stati$type == "Prison St Michel",],
           "Purpan" = df_Stati[df_Stati$type == "Purpan",],
           "Ramonville" = df_Stati[df_Stati$type == "Ramonville",],
           "Rangueil" = df_Stati[df_Stati$type == "Rangueil",],
           "Roseraie" = df_Stati[df_Stati$type == "Roseraie",],
           "Saint Cyprien" = df_Stati[df_Stati$type == "Saint Cyprien",],
           "Thales AlÃ©ria" = df_Stati[df_Stati$type == "Thales Aléria",],
           "Tournefeuille" = df_Stati[df_Stati$type == "Tournefeuille",],
           "Wilson" = df_Stati[df_Stati$type == "Wilson",]
    )
  })
  
  #Selection des courses en fonction du chauffeur selectionné
  output$selection <- renderUI ({
    selectInput("selcourses","Courses",
                choices = levels(as.factor(as.numeric(df_trajCourses$num[df_trajCourses$condu == input$selcondu]))), 
                selected = levels(as.factor(as.numeric(df_trajCourses$num[df_trajCourses$condu == input$selcondu])))[1])
  })
  
  
  #Selection du condducteurs en fonction de la station selectionnée
  output$reac_sel_condu_stati <- renderUI({
    selectInput("selcondu","Conducteurs",
                choices = Conducteurs$nom[Conducteurs$station == input$selstation], selected = Conducteurs$nom[Conducteurs$station == input$selstation][1])
  })
 
  ################### CARTES #############################
  
  # Carte conducteurs
  output$MapTraj <- renderLeaflet({
    #Défition de la carte
    map <- leaflet() %>%
      #Ajout de la carte du monde
      addTiles() %>%
      #Ajout des marqueurs sur les conducteurs
      addCircleMarkers(data = df_Traj[df_Traj$nom == input$selcondu,],
                       stroke = FALSE, fillOpacity = 1)
    #Affichage de la carte
    map
  })
  
  output$MapTrajCourses <- renderLeaflet({
    #Défition de la carte
    map <- leaflet() %>%
      #Ajout de la carte du monde
      addTiles() %>%
      #Ajout des marqueurs sur les conducteurs
      addCircleMarkers(data = df_trajCourses[df_trajCourses$condu == input$selcondu & df_trajCourses$num == input$selcourses,],
                       stroke = FALSE, fillOpacity = 1,radius = 3)
    #Affichage de la carte
    map
  })
  
  ## Carte clients
  output$MapClien <- renderLeaflet({
    map <- leaflet() %>% 
      addTiles() %>%
      setView(lng = 1.43333, lat=43.6, zoom = 12) %>%
      addMarkers(data = df_clien, icon = Ic_personn) 
    map
  })
  
  
  #Carte Nombre de taxi par stations
  output$MapStati <- renderLeaflet({
    map <- leaflet() %>% 
      addTiles() %>%
      addCircles(data = Stations(),
                 radius = c(Stations()$entree,Stations()$sortie),
                 fillOpacity = 0.1,
                 opacity = 1) %>%
      #Ajout de cerle pour les stations
      addCircleMarkers(data = Stations(),
                       #Nom de la station
                       popup = paste(Stations()$type,Stations()$nb,'taxis disponibles'),
                       #Couleur associées aux points en fonction de la valeur du nb de taxi
                       color = ~pal(nb),
                       #Options d'affichages
                       stroke = FALSE, fillOpacity = 0.7) %>%
      #Légende pour les couleurs
      addLegend("bottomright", pal = pal, values = Stations()$nb,
                title = "Nombre de taxis",
                opacity = 1
      )
    map
  })
  
  ############################### Graphiques ################################
  
  
  #CA journalier
  output$plotCA <- renderPlotly({
    ggplotly(CAj)
  })
  
  #Nb de course par jour
  output$plotNBc <- renderPlotly({
    ggplotly(NBc)
  })
  
  #CA moyen par jour et par course
  output$plotCAmoy <- renderPlotly({
    ggplotly(CAmoy)
  })
  
#   #Pourcentage de conducteurs par station
#   output$plotPctConduStat <- renderPlot({
#     barplot(tabPctConduStat, col = "#DF73FF",main="Pct de conducteur par station",ylim=c(0,100),cex.names=1,4 )
#   })
#   
#   #Type de paiement en fonction du montant
#   output$plotTypePaiMontant <- renderPlotly({
#     ggplotly(G_TypePaiMontant)
#   })
#   
#   #Différence entre les estimations en fonction de l'heure de départ
#   output$plotDifEstimHDep <- renderPlotly({
#     ggplotly(G_DifEstimHDep)
#   })

  

  
  
})