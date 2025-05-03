library(DBI)
library(odbc)
library(yaml)

config <- yaml::read_yaml("c:/Projetos/Estudos/FIAP/Cap 1 - Construindo uma máquina agrícola/config.yaml")
sql_conf <- config$mssql

con <- dbConnect(odbc::odbc(),
  Driver   = sql_conf$driver,
  Server   = sql_conf$host,
  Port     = sql_conf$port,
  Database = sql_conf$database,
  Encryption = "no",
  Trusted_Connection = "Yes",
  TrustServerCertificate = "yes"
)