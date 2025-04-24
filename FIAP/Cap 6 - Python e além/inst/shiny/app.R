library(shiny)
library(DBI)
library(AgroDataR)

# Conexão Oracle (exemplo com ROracle)
con <- DBI::dbConnect(ROracle::Oracle(),
                     username = Sys.getenv("ORACLE_USER"),
                     password = Sys.getenv("ORACLE_PASS"),
                     dbname   = Sys.getenv("ORACLE_DSN"))

ui <- fluidPage(
  titlePanel("Dashboard de Insumos Agrícolas"),
  sidebarLayout(
    sidebarPanel(
      helpText("Visão geral dos insumos por cultura")
    ),
    mainPanel(
      plotOutput("insumosPlot")
    )
  )
)

server <- function(input, output, session) {
  df_insumos <- get_summary_insumos(con)
  output$insumosPlot <- renderPlot({
    plot_insumos(df_insumos)
  })
}

shinyApp(ui, server)
