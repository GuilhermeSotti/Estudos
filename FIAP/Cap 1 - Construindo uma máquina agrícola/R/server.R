source("Cap 1 - Construindo uma máquina agrícola/R/modules/plots.R")
source("Cap 1 - Construindo uma máquina agrícola/R/modules/table.R")

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

  humidity_df  <- reactive({ readings() %>% filter(sensor_id == 2) })
  ph_df        <- reactive({ readings() %>% filter(sensor_id == 1) })
  nutrients_df <- reactive({
    readings() %>%
      filter(sensor_id %in% c(3,4)) %>%
      mutate(nutriente = ifelse(sensor_id == 3, "P", "K"))
  })

  output$plot_humidity <- renderPlot({
    df <- humidity_df()
    ggplot(df, aes(x = timestamp, y = valor)) +
      geom_line() +
      labs(x = "Hora", y = "Umidade (%)", title = "Umidade do Solo ao Longo do Tempo")
  })

  output$plot_pH <- renderPlot({
    df <- ph_df()
    ggplot(df, aes(x = timestamp, y = valor)) +
      geom_line() +
      labs(x = "Hora", y = "pH", title = "pH do Solo ao Longo do Tempo")
  })

  output$plot_nutrients <- renderPlot({
    df <- nutrients_df()
    ggplot(df, aes(x = timestamp, y = valor, color = nutriente)) +
      geom_step() +
      labs(x = "Hora", y = "Presença (0 = Ausente; 1 = Presente)",
           title = "Presença de Fósforo (P) e Potássio (K)", color = "Nutriente")
  })

  output$table_logs <- DT::renderDT({
    readings() %>%
      arrange(desc(timestamp))
  }, options = list(pageLength = 10, scrollX = TRUE))
}