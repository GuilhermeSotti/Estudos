library(shiny)
library(shinydashboard)

source("c:/Projetos/Estudos/FIAP/Cap 1 - Construindo uma máquina agrícola/R/modules/mod_table.R")
source("c:/Projetos/Estudos/FIAP/Cap 1 - Construindo uma máquina agrícola/R/modules/mod_plots.R")

ui <- dashboardPage(
  dashboardHeader(title = "FarmTech Dashboard"),
  dashboardSidebar(
    dateRangeInput("periodo", "Período de Leituras",
                   start = Sys.Date() - 7, end = Sys.Date()),
    checkboxGroupInput("sensores", "Sensores",
                       choices = c("pH" = 1, "Umidade" = 2, "P" = 3, "K" = 4),
                       selected = c(1,2,3,4)),
    sidebarMenu(
      menuItem("Dashboard", tabName = "dashboard", icon = icon("dashboard"))
    )
  ),
  dashboardBody(
    fluidRow(
      valueBoxOutput("current_ph"),
      valueBoxOutput("current_humidity")
    ),
    tabItems(
      tabItem(tabName = "dashboard",
        fluidRow(
          box(width = 6, title = "Umidade (%)", status = "primary", solidHeader = TRUE,
              mod_plotUI("umidade")
          ),
          box(width = 6, title = "pH", status = "primary", solidHeader = TRUE,
              mod_plotUI("ph")
          )
        ),
        fluidRow(
          box(width = 12, title = "Nutrientes P e K", status = "primary", solidHeader = TRUE,
              mod_plotUI("nutrientes")
          )
        ),
        fluidRow(
          box(width = 12, title = "Log de Leituras", status = "info", solidHeader = TRUE,
              mod_tableUI("logs")
          )
        )
      )
    )
  )
)
