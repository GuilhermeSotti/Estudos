library(shiny)
library(shinydashboard)
library(DBI)
library(odbc)
library(dplyr)
library(ggplot2)
library(DT)

con <- dbConnect(
  odbc::odbc(),
  Driver   = "ODBC Driver 18 for SQL Server",
  Server   = "localhost,1433",
  Database = "FarmTechDB",
  UID      = "sa",
  PWD      = "admin!1234",
  TrustServerCertificate = "yes"
)