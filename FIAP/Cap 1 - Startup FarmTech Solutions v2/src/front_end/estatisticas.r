library(jsonlite)

dados <- fromJSON("data/dados_farmtech.json")

areas <- sapply(dados, function(x) x$area)
insumos <- sapply(dados, function(x) x$insumo$quantidade)

media_area <- mean(areas)
dp_area <- sd(areas)

media_insumo <- mean(insumos)
dp_insumo <- sd(insumos)

cat("===== Estatísticas dos Dados =====\n")
cat("Média da Área: ", media_area, "\n")
cat("Desvio Padrão da Área: ", dp_area, "\n")
cat("Média do Insumo: ", media_insumo, "\n")
cat("Desvio Padrão do Insumo: ", dp_insumo, "\n")
