#' Coleta dados COMEXSTAT e grava em raw/Oracle
#'
#' @param product_code string, código NCM ou similar
#' @param year integer, ano a coletar
#' @param flow string, "Export" ou "Import"
#' @param con conexão DBI válida ao Oracle
#' @return data.frame com os dados coletados
#' @import httr jsonlite DBI
#' @export
ingest_comexstat <- function(product_code, year, flow = "Export", con) {
  base_url <- "http://comexstat.mdic.gov.br/Service/Commerce/Query"
  resp <- httr::GET(base_url,
                    query = list(produto = product_code,
                                 ano     = year,
                                 fluxo   = tolower(flow)),
                    timeout = 30)
  httr::stop_for_status(resp)
  json <- httr::content(resp, as = "text", encoding = "UTF-8")
  df <- jsonlite::fromJSON(json)$Retorno
  # grava raw payload em tabela Oracle
  DBI::dbExecute(con,
    "INSERT INTO raw_data.tb_comexstat_raw (source, ingest_ts, payload)
     VALUES (:1, SYSTIMESTAMP, :2)",
    params = list("COMEXSTAT", jsonlite::toJSON(df, auto_unbox = TRUE))
  )
  return(df)
}
