source("estatisticas.R")
source("api_meteorologia.R")

cat("=== Executando Análise Estatística ===\n")

cat("\n=== Consultando API Meteorológica ===\n")
consultar_api_meteorologia(cidade = "Sao Paulo", api_key = "YOUR_API_KEY")