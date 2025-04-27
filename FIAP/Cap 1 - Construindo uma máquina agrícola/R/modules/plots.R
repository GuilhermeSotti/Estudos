library(ggplot2)

plot_humidity <- function(df) {
  ggplot(df, aes(x = timestamp, y = valor)) +
    geom_line() +
    labs(
      x     = "Hora",
      y     = "Umidade (%)",
      title = "Umidade do Solo ao Longo do Tempo"
    ) +
    theme_minimal()
}

plot_pH <- function(df) {
  ggplot(df, aes(x = timestamp, y = valor)) +
    geom_line() +
    labs(
      x     = "Hora",
      y     = "pH",
      title = "pH do Solo ao Longo do Tempo"
    ) +
    theme_minimal()
}

plot_nutrients <- function(df) {
  ggplot(df, aes(x = timestamp, y = valor, color = nutriente)) +
    geom_step() +
    labs(
      x      = "Hora",
      y      = "Presença (0 = Ausente; 1 = Presente)",
      title  = "Presença de Fósforo (P) e Potássio (K)",
      color  = "Nutriente"
    ) +
    theme_minimal()
}
