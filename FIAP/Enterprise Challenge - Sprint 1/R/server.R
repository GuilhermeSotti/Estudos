library(shiny)
library(dplyr)
library(ggplot2)
library(DT)

sserver <- function(input, output, session) {
  data <- reactive({
    influx_select(con, db = db_name, measurement = measurement,
                  limit = 100, order = "desc") %>%
      mutate(time = ymd_hms(time)) %>%
      arrange(time)
  })
  
  output$timeseriesPlot <- renderPlotly({
    df <- data()
    p <- df %>% 
      plot_ly(x = ~time) %>%
      add_lines(y = ~temperature, name = "Temperature") %>%
      add_lines(y = ~vibration, name = "Vibration") %>%
      layout(title = "Últimos 100 registros",
             xaxis = list(title = "Timestamp"),
             yaxis = list(title = "Value"))
    p
  })
}