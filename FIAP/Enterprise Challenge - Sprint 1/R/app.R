install.packages(c(
  "shiny",
  "influxdbr",
  "dplyr",
  "lubridate",
  "plotly",
  "httr",
  "jsonlite"
))

library(shiny)
library(influxdbr)
library(dplyr)
library(lubridate)
library(plotly)
library(httr)
library(jsonlite)

source("c:/Projetos/Estudos/FIAP/Enterprise Challenge - Sprint 1/R/global.R")
source("c:/Projetos/Estudos/FIAP/Enterprise Challenge - Sprint 1/R/server.R")
source("c:/Projetos/Estudos/FIAP/Enterprise Challenge - Sprint 1/R/ui.R")

shinyApp(ui, server)