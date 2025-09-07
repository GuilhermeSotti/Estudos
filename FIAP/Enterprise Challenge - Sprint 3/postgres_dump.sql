CREATE TABLE IF NOT EXISTS machine (
  machine_id SERIAL PRIMARY KEY,
  code VARCHAR(64) UNIQUE NOT NULL,
  location VARCHAR(128),
  installed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sensor (
  sensor_id SERIAL PRIMARY KEY,
  machine_id INT NOT NULL REFERENCES machine(machine_id) ON DELETE CASCADE,
  type VARCHAR(32) NOT NULL,
  unit VARCHAR(16),
  sampling_hz NUMERIC(10,2),
  created_at TIMESTAMP DEFAULT now(),
  UNIQUE (machine_id, type)
);

CREATE TABLE IF NOT EXISTS reading (
  reading_id BIGSERIAL PRIMARY KEY,
  sensor_id INT NOT NULL REFERENCES sensor(sensor_id) ON DELETE CASCADE,
  ts TIMESTAMP NOT NULL,
  value DOUBLE PRECISION NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_reading_sensor_ts ON reading(sensor_id, ts);

CREATE TABLE IF NOT EXISTS failure_event (
  failure_id BIGSERIAL PRIMARY KEY,
  machine_id INT NOT NULL REFERENCES machine(machine_id) ON DELETE CASCADE,
  start_ts TIMESTAMP NOT NULL,
  end_ts TIMESTAMP,
  failure_type VARCHAR(64),
  notes TEXT
);

CREATE TABLE IF NOT EXISTS ml_inference (
  inference_id BIGSERIAL PRIMARY KEY,
  machine_id INT NOT NULL REFERENCES machine(machine_id) ON DELETE CASCADE,
  ts TIMESTAMP NOT NULL,
  model_name VARCHAR(64) NOT NULL,
  class_prob NUMERIC(10,6),
  predicted_label SMALLINT,
  rul_minutes NUMERIC(10,2),
  extra JSONB
);
CREATE INDEX IF NOT EXISTS ix_inference_machine_ts ON ml_inference(machine_id, ts);
