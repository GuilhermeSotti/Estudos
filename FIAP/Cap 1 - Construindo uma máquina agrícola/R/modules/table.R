library(DT)
library(dplyr)

render_logs_table <- function(df) {
  df %>%
    arrange(desc(timestamp)) %>%
    DT::datatable(
      options = list(
        pageLength = 10,
        scrollX    = TRUE
      ),
      rownames = FALSE
    )
}
