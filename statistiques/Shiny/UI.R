library(shiny)
library(leaflet)
library(magrittr)
library(leaflet)
library(plotly)
source("extractAPI.R")
# Define UI for dataset viewer application
shinyUI(fluidPage(
  
  # Application title
  titlePanel("TaxiSid Toulouse"),
  
  # Sidebar with controls 
  sidebarLayout(
    sidebarPanel(
      #Selection de la station
      selectInput("selstation","Stations",
                  choices = c("Toutes",levels(df_Stati$type)), selected = "Toutes"),
      #Affichage des chauffeurs de la station selectionnee
      uiOutput("reac_sel_condu_stati")
    ),
    
    # Affichage principal
    mainPanel(
      #Liste d onglets
      tabsetPanel(
        #Onglets
        tabPanel("Conducteur", #Titre de l'onglet
                 # Titre
                 h1("Trajet de la journee"),
                 # Carte trajet d'un conducteur dans la journee
                 leafletOutput("MapTraj", width = "100%", height="500")
                 ),
        tabPanel("Clients", h1("Positions clients"),
                 # Carte situant les clients
                 leafletOutput("MapClien", width = "100%", height="500")),
        tabPanel("Stations", h1("Nombre de taxis disponibles par stations"),
                 # CArte du nombre de taxis par stations (rajouter statut)
                 leafletOutput("MapStati", width = "100%", height="500")
                 # Pourcentage de conducteurs par station
                 #plotOutput("plotPctConduStat")
                 ),
        tabPanel("Courses", h1("Courses"),
                 # Ligne avec plusieurs element
                 fluidRow(
                   # Element vide
                   column(6),
                   # Selection de la course en fonction du chauffeur selectionne
                   column(6,uiOutput("selection"))
                 ),
                 #Carte du trajet de la course selectionnee du conducteur selectionne
                 leafletOutput("MapTrajCourses", width = "100%", height="500")),
        tabPanel("Factures",
                 #Ca par jours
                 plotlyOutput("plotCA"),
                 #Nb de courses par jours
                 plotlyOutput("plotNBc"),
                 #CA moyen par jours et par courses
                 plotlyOutput("plotCAmoy")
#                  #Type de paiement par montant
#                  plotlyOutput("plotTypePaiMontant"),
#                  #Difference entre les estimations en fonction de l'heure de depart
#                  plotlyOutput("plotDifEstimHDep")
#                  )        
        )
        
      )
    )
)))