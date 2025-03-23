source("FIAP\\Cap 1 - Startup FarmTech Solutions v2\\src\\front_end\\api_meteorologia.R")
source("FIAP\\Cap 1 - Startup FarmTech Solutions v2\\src\\front_end\\estatisticas.R")

cat("=== Executando Análise Estatística ===\n")

cat("\n=== Consultando API Meteorológica ===\n")
consultar_api_meteorologia(cidade_html = "Sao%20Paulo", cidade = "Sao Paulo", api_key = "66f8aa7fe075bab3f34048b46f40b64c")

cat("\n=== Criando Dashboards ===\n")
criar_dahsboards(path_json = "FIAP\\Cap 1 - Startup FarmTech Solutions v2\\data\\dados_farmtech.json")