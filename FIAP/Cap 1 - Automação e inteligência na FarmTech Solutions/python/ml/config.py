import os
from pathlib import Path
import yaml

DB_URI = os.getenv("DB_URI", "sqlite:///../farmtech.db")
if DB_URI is None:
    cfg_path = Path(__file__).parent.parent / "config.yaml"
    try:
        with open(cfg_path, 'r') as f:
            cfg = yaml.safe_load(f)
        DB_URI = cfg.get("db_uri")
    except FileNotFoundError:
        DB_URI = None
    except Exception as e:
        raise RuntimeError(f"Erro ao ler config.yaml em {cfg_path}: {e}")

ROOT_DIR = Path(__file__).parent.parent
MODEL_DIR = ROOT_DIR / "models"
MODEL_PATH = MODEL_DIR / "irrigation_model.joblib"

RF_PARAMS = {
    "n_estimators": 100,
    "max_depth": None,
    "random_state": 42,
    "n_jobs": -1
}