CREATE TABLE IF NOT EXISTS machine (
  machine_id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT UNIQUE NOT NULL,
  location TEXT,
  installed_at DATETIME
);

CREATE TABLE IF NOT EXISTS sensor (
  sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
  machine_id INTEGER NOT NULL,
  type TEXT NOT NULL,
  unit TEXT,
  sampling_hz REAL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (machine_id, type),
  FOREIGN KEY (machine_id) REFERENCES machine(machine_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reading (
  reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
  sensor_id INTEGER NOT NULL,
  ts DATETIME NOT NULL,
  value REAL NOT NULL,
  FOREIGN KEY (sensor_id) REFERENCES sensor(sensor_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_reading_sensor_ts ON reading(sensor_id, ts);

CREATE TABLE IF NOT EXISTS failure_event (
  failure_id INTEGER PRIMARY KEY AUTOINCREMENT,
  machine_id INTEGER NOT NULL,
  start_ts DATETIME NOT NULL,
  end_ts DATETIME,
  failure_type TEXT,
  notes TEXT,
  FOREIGN KEY (machine_id) REFERENCES machine(machine_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ml_inference (
  inference_id INTEGER PRIMARY KEY AUTOINCREMENT,
  machine_id INTEGER NOT NULL,
  ts DATETIME NOT NULL,
  model_name TEXT NOT NULL,
  class_prob REAL,
  predicted_label INTEGER,
  rul_minutes REAL,
  extra TEXT,
  FOREIGN KEY (machine_id) REFERENCES machine(machine_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_inference_machine_ts ON ml_inference(machine_id, ts);
