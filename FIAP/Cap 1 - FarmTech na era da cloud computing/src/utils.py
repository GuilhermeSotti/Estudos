import joblib
import json
import logging
import os
from datetime import datetime

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

def setup_logging(name="farmtech", level=logging.INFO, log_file=None):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(ch)
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(fh)
    return logger

logger = setup_logging(log_file=f"logs/farmtech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

def save_model(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    logger.info(f"Modelo salvo em {path}")

def load_model(path):
    if not os.path.exists(path):
        logger.error(f"Modelo não encontrado: {path}")
        raise FileNotFoundError(path)
    model = joblib.load(path)
    logger.info(f"Modelo carregado de {path}")
    return model

def save_json(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    logger.info(f"JSON salvo em {path}")

def load_json(path):
    if not os.path.exists(path):
        logger.error(f"JSON não encontrado: {path}")
        raise FileNotFoundError(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
