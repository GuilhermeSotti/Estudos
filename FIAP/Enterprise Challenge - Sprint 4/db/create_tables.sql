CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS devices (
  device_id TEXT PRIMARY KEY,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS measurements (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  device_id TEXT REFERENCES devices(device_id),
  ts TIMESTAMP NOT NULL,
  temperature_c NUMERIC,
  humidity NUMERIC
);
CREATE INDEX ON measurements (device_id, ts);

CREATE TABLE IF NOT EXISTS alerts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  device_id TEXT,
  ts TIMESTAMP DEFAULT now(),
  alert_type TEXT,
  value NUMERIC,
  message TEXT
);

CREATE TABLE IF NOT EXISTS ml_runs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  run_ts TIMESTAMP DEFAULT now(),
  model_type TEXT,
  metric_name TEXT,
  metric_value NUMERIC,
  notes TEXT
);
