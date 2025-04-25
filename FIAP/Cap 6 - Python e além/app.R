install.packages(c("shiny", "DBI", "odbc", "yaml", "DT"))

library(shiny)
library(DBI)
library(odbc)
library(yaml)
library(DT)

source("C:/Projetos/Estudos/FIAP/Cap 6 - Python e além/R/dashboard.R")

config <- yaml::read_yaml("C:/Projetos/Estudos/FIAP/Cap 6 - Python e além/python/config/config.yaml")
sql_conf <- config$mssql

con <- dbConnect(odbc::odbc(),
                 Driver   = sql_conf$driver,
                 Server   = sql_conf$host,
                 Port     = sql_conf$port,
                 Database = sql_conf$database,
                 Encryption = "no",
                 Trusted_Connection = "Yes",
                 TrustServerCertificate = "yes")

ui <- fluidPage(
  titlePanel("Dashboard de Insumos por Cultura"),
  sidebarLayout(
    sidebarPanel(helpText("Quantidade total de insumos agrupados por cultura e país")),
    mainPanel(
      plotOutput("insumosPlot"),
      DTOutput("summaryTable")
    )
  )
)

server <- function(input, output, session) {
  df <- dbGetQuery(con, "
    SELECT TOP 3 cultura, SUM(quantidade) AS total 
    FROM staging.stg_insumos 
    GROUP BY cultura
  ")
  
  summary_df <- get_summary_by_country(con)
  
  output$insumosPlot <- renderPlot({
    barplot(
      height = df$total,
      names.arg = df$cultura,
      col = "darkgreen",
      las = 2,                
      main = "Quantidade por Cultura",
      ylab = "Quantidade",
      cex.names = 0.7,
      border = NA,
      space = 0.5
    )
  })
  
  output$summaryTable <- renderDT({
    render_summary_table(summary_df)
  })
}

shinyApp(ui = ui, server = server)
