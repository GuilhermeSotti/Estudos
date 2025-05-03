library(shiny)
library(dplyr)
library(ggplot2)
library(DT)

source("c:/Projetos/Estudos/FIAP/Cap 1 - Construindo uma máquina agrícola/R/modules/mod_table.R")
source("c:/Projetos/Estudos/FIAP/Cap 1 - Construindo uma máquina agrícola/R/modules/mod_plots.R")

server <- function(input, output, session) {

  readings <- reactivePoll(
    5000, session,
    checkFunc = function() {
      dbGetQuery(con, "SELECT MAX(leitura_id) AS id FROM Monitoring.LeituraDoSensor")$id
    },
    valueFunc = function() {
      dbGetQuery(con, "SELECT leitura_id, sensor_id, valor, timestamp FROM Monitoring.LeituraDoSensor ORDER BY timestamp")
    }
  )

  filtered <- reactive({
    readings() %>%
      filter(sensor_id %in% input$sensores,
             as.Date(timestamp) >= input$periodo[1],
             as.Date(timestamp) <= input$periodo[2])
  })

  humidity_df  <- reactive({ filtered() %>% filter(sensor_id == 2) })
  ph_df        <- reactive({ filtered() %>% filter(sensor_id == 1) })
  nutrients_df <- reactive({
    filtered() %>% 
      filter(sensor_id %in% c(3,4)) %>%
      mutate(nutriente = ifelse(sensor_id == 3, "P", "K"))
  })

  output$current_ph <- renderValueBox({
    val <- tail(ph_df()$valor, 1)
    valueBox(
      round(val,2), "pH Atual", icon = icon("flask"),
      color = if (val < 6) "orange" else "green"
    )
  })
  output$current_humidity <- renderValueBox({
    val <- tail(humidity_df()$valor,1)
    valueBox(
      paste0(round(val,2),"%"), "Umidade Atual", icon = icon("tint"),
      color = if (val > 90) "red" else "blue"
    )
  })

  mod_plotServer("umidade",
    df        = humidity_df,
    aes_args  = list(x = "timestamp", y = "valor"),
    labs_args = list(x = "Hora", y = "Umidade (%)", title = "Umidade do Solo")
  )
  mod_plotServer("ph",
    df        = ph_df,
    aes_args  = list(x = "timestamp", y = "valor"),
    labs_args = list(x = "Hora", y = "pH", title = "pH do Solo")
  )
  mod_plotServer("nutrientes",
    df        = nutrients_df,
    aes_args  = list(x = "timestamp", y = "valor", colour = "nutriente"),
    labs_args = list(x = "Hora", y = "Presença (0/1)", title = "P e K", colour_label = "Nutriente"),
    geom_fun  = geom_step
  )

  mod_tableServer("logs", df = filtered)
}
