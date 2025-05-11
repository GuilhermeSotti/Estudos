import os

# MQTT
MQTT_BROKER = os.getenv("MQTT_BROKER", "a1b2c3.iot.us-east-1.amazonaws.com")
MQTT_PORT   = int(os.getenv("MQTT_PORT", 8883))
MQTT_TOPIC  = os.getenv("MQTT_TOPIC", "industrial/sensors")

# AWS
AWS_REGION    = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET     = os.getenv("S3_BUCKET", "my-data-lake-bucket")
REDSHIFT_HOST = os.getenv("REDSHIFT_HOST", "redshift.cluster.amazonaws.com")
GLUE_JOB_NAME = os.getenv("GLUE_JOB_NAME", "industrial-etl-job")

# Database Time-Series
TSDB_ENDPOINT = os.getenv("TSDB_ENDPOINT", "https://influxdb.example.com")

# Model Registry / Docker Registry
MODEL_REGISTRY_URI = os.getenv("MODEL_REGISTRY_URI", "123456789012.dkr.ecr.us-east-1.amazonaws.com")

# Slack / Notifications
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
