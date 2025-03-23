library(jsonlite)
library(ggplot2)

criar_dahsboards <- function(path_json) {
    dados <- fromJSON(path_json, simplifyDataFrame = FALSE)

    df <- data.frame(
        Cultura = sapply(dados, function(x) x$cultura),
        Area = sapply(dados, function(x) x$area),
        Insumo = sapply(dados, function(x) x$insumo$quantidade)
    )

    media_area <- mean(df$Area)
    dp_area <- sd(df$Area)
    media_insumo <- mean(df$Insumo)
    dp_insumo <- sd(df$Insumo)

    cat("===== Estatísticas dos Dados =====\n")
    cat("Média da Área: ", media_area, "\n")
    cat("Desvio Padrão da Área: ", dp_area, "\n")
    cat("Média do Insumo: ", media_insumo, "\n")
    cat("Desvio Padrão do Insumo: ", dp_insumo, "\n")

    ggplot(df, aes(x = Area)) + 
    geom_histogram(binwidth = 100, fill = "blue", color = "white", alpha = 0.7) + 
    geom_vline(aes(xintercept = media_area), color = "red", linetype = "dashed") + 
    labs(
        title = "Distribuição das Áreas das Plantações",
        x = "Área (m²)",
        y = "Frequência"
    ) + theme_minimal()

    ggsave("histograma_areas.png", width = 10, height = 10)

    ggplot(df, aes(x = Cultura, y = Insumo, fill = Cultura)) + 
    geom_bar(stat = "identity", color = "white", alpha = 0.7) + 
    labs(
        title = "Quantidade de Insumo por Cultura",
        x = "Cultura",
        y = "Quantidade de Insumo"
    ) + theme_minimal()

    ggsave("barras_insumo.png", width = 10, height = 10)
}