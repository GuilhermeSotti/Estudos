library(shinydashboard)

ui <- dashboardPage(
  dashboardHeader(title = "FarmTech Dashboard"),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Dashboard", tabName = "dashboard", icon = icon("dashboard"))
    )
  ),
  dashboardBody(
    tabItems(
      tabItem(tabName = "dashboard",
        fluidRow(
          box(title = "Umidade (%)", status = "primary",
              solidHeader = TRUE, width = 6,
              plotOutput("plot_humidity", height = "250px")
          ),
          box(title = "pH", status = "primary",
              solidHeader = TRUE, width = 6,
              plotOutput("plot_pH", height = "250px")
          )
        ),
        fluidRow(
          box(title = "Nutrientes P e K", status = "primary",
              solidHeader = TRUE, width = 12,
              plotOutput("plot_nutrients", height = "250px")
          )
        ),
        fluidRow(
          box(title = "Log de Leituras", status = "info",
              solidHeader = TRUE, width = 12,
              DTOutput("table_logs")
          )
        )
      )
    )
  )
)