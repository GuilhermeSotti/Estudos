install.packages(c("shiny", "ggplot2", "DBI", "odbc", "yaml", "DT", "dplyr", "shinydashboard"))

library(shiny)
library(DBI)
library(odbc)
library(ggplot2)
library(DT)
library(yaml)

source("c:/Projetos/Estudos/FIAP/Cap 1 - Construindo uma máquina agrícola/R/global.R")
source("c:/Projetos/Estudos/FIAP/Cap 1 - Construindo uma máquina agrícola/R/server.R")
source("c:/Projetos/Estudos/FIAP/Cap 1 - Construindo uma máquina agrícola/R/ui.R")

shinyApp(ui, server)
