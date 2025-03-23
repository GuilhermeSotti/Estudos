library(httr)
library(jsonlite)

consultar_api_meteorologia <- function(cidade_html = "Sao%20Paulo", cidade = "Sao Paulo", api_key) {
  url <- paste0("http://api.openweathermap.org/data/2.5/weather?q=", cidade_html,
                "&appid=", api_key, "&units=metric", "&lang=pt_br")
  resposta <- GET(url)
  
  if (resposta$status_code == 200) {
    dados <- fromJSON(content(resposta, "text", encoding = "UTF-8"))
    cat("===== Dados Meteorológicos para", cidade, "=====\n")
    cat("Temperatura: ", dados$main$temp, "°C\n")
    cat("Sensação Térmica: ", dados$main$feels_like, "°C\n")
    cat("Umidade: ", dados$main$humidity, "%\n")
    cat("Condição: ", dados$weather$description, "\n")
  } else {
    cat("Falha ao obter dados meteorológicos.\n")
  }
}