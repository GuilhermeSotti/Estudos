#' Coleta dados FAOSTAT e grava em raw/Oracle
#'
#' @param dataset string, nome do dataset FAOSTAT (ex: "production_crops")
#' @param year integer, ano a coletar (ex: 2022)
#' @param con conexão DBI válida ao Oracle
#' @return data.frame com os dados coletados
#' @import httr jsonlite DBI
#' @export
ingest_faostat <- function(dataset, year, con) {
  base_url <- "https://api.fao.org/faostat/v1"
  url <- paste0(base_url, "/", dataset)
  resp <- httr::GET(url, query = list(year = year), timeout(30))
  httr::stop_for_status(resp)
  json <- httr::content(resp, as = "text", encoding = "UTF-8")
  df <- jsonlite::fromJSON(json)$data
  # grava raw payload em tabela Oracle
  DBI::dbExecute(con,
    "INSERT INTO raw_data.tb_faostat_raw (source, ingest_ts, payload)
     VALUES (:1, SYSTIMESTAMP, :2)",
    params = list("FAOSTAT", jsonlite::toJSON(df, auto_unbox = TRUE))
  )
  return(df)
}
