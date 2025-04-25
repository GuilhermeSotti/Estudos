#' Funções auxiliares para dashboard Shiny
#'
#' @import dplyr
#' @export
get_summary_insumos <- function(con) {
  DBI::dbGetQuery(con, "
    SELECT c.nome, AVG(quantidade) AS preco_medio
    FROM analytics.fact_colheita as fc
    INNER JOIN analytics.dim_cultura as c ON c.cultura_id = fc.cultura_id
    GROUP BY c.nome
  ")
}

#' Exemplo de plot com ggplot2
#' @import ggplot2
#' @export
plot_insumos <- function(df) {
  ggplot2::ggplot(df, ggplot2::aes(x = cultura, y = preco_medio)) +
    ggplot2::geom_col() +
    ggplot2::theme_minimal() +
    ggplot2::labs(title = "Preço Médio de Insumos por Cultura")
}

#' Função para obter resumo de insumos por país
#' @export
get_summary_by_country <- function(con) {
  DBI::dbGetQuery(con, "
    SELECT pais, SUM(quantidade) AS total_insumos
    FROM staging.stg_insumos
    GROUP BY pais
  ")
}

#' Função para renderizar tabela de resumo
#' @import DT
#' @export
render_summary_table <- function(df) {
  DT::datatable(df, options = list(pageLength = 5), rownames = FALSE)
}
