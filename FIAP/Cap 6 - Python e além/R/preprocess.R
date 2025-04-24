#' Remove colunas com alta proporção de NA
#' @param df data.frame
#' @param thresh numeric entre 0 e 1, proporção mínima de dados não NA
#' @return data.frame
#' @export
drop_missing <- function(df, thresh = 0.8) {
  min_count <- thresh * nrow(df)
  df[, colSums(!is.na(df)) >= min_count, drop = FALSE]
}

#' Preenche valores faltantes com defaults
#' @param df data.frame
#' @param defaults named list de valores padrão (col = valor)
#' @return data.frame
#' @export
fill_defaults <- function(df, defaults = list()) {
  for (col in names(defaults)) {
    df[[col]][is.na(df[[col]])] <- defaults[[col]]
  }
  df
}

#' Normaliza colunas numéricas no intervalo [0,1]
#' @param df data.frame
#' @param cols character vector, nomes das colunas
#' @return data.frame
#' @export
normalize_numeric <- function(df, cols) {
  for (col in cols) {
    min_val <- min(df[[col]], na.rm = TRUE)
    max_val <- max(df[[col]], na.rm = TRUE)
    df[[col]] <- (df[[col]] - min_val) / (max_val - min_val)
  }
  df
}

#' Aplica one-hot encoding em colunas categóricas
#' @param df data.frame
#' @param cols character vector, nomes das colunas
#' @return data.frame
#' @export
encode_categorical <- function(df, cols) {
  tidyr::pivot_wider(
    tidyr::pivot_longer(df, cols),
    names_from  = name,
    values_from = value,
    values_fill = list(value = 0),
    names_sep   = "_"
  )
}
