#' Funções auxiliares para dashboard Shiny
#'
#' @import dplyr
#' @export
get_summary_insumos <- function(con) {
  DBI::dbGetQuery(con, "
    SELECT cultura, AVG(preco) AS preco_medio
    FROM analytics.fact_insumos
    GROUP BY cultura
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
