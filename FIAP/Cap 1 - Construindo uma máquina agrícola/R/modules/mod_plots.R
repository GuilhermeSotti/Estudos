#' @export
mod_plotUI <- function(id) {
  ns <- NS(id)
  plotOutput(ns("plot"), height = "250px")
}

#' @export
mod_plotServer <- function(id, df, aes_args, labs_args, geom_fun = geom_line) {
  moduleServer(id, function(input, output, session) {
    output$plot <- renderPlot({
      p <- ggplot(df(), aes_string(x = aes_args$x, y = aes_args$y))
      if (!is.null(aes_args$colour)) {
        p <- p + aes_string(colour = aes_args$colour)
      }
      p + geom_fun() +
        labs(x = labs_args$x,
             y = labs_args$y,
             title = labs_args$title,
             color = labs_args$colour_label %||% NULL) +
        theme_minimal()
    })
  })
}
