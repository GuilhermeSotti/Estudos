library(shiny)
library(shinydashboard)

ui <- fluidPage(
  titlePanel("🌡️ Monitoramento Industrial (R/Shiny)"),
  fluidRow(
    column(12,
      plotlyOutput("timeseriesPlot")
    )
  ),
  fluidRow(
    column(2,
      actionButton("alert_btn", "Forçar Alerta", icon = icon("bell"))
    )
  )
)