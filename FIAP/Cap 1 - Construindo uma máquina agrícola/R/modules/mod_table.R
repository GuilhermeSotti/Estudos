#' @export
mod_tableUI <- function(id) {
  ns <- NS(id)
  DTOutput(ns("table"))
}

#' @export
mod_tableServer <- function(id, df) {
  moduleServer(id, function(input, output, session) {
    output$table <- renderDT({
      df() %>% arrange(desc(timestamp))
    }, options = list(pageLength = 10, scrollX = TRUE))
  })
}
