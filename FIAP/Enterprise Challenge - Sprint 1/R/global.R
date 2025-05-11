library(influxdbr)

influx_host <- Sys.getenv("TSDB_ENDPOINT")
db_name <- "industrial_ts"
measurement <- "sensor_readings"

# Conexão ao InfluxDB
con <- influx_connection(host = influx_host, port = 8086)