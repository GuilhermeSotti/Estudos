import os
from pathlib import Path

DB_URI = os.getenv("DB_URI", "sqlite:///../farmtech.db")

MODEL_DIR = Path(__file__).parent / "export"
MODEL_PATH = MODEL_DIR / "irrigation_model.joblib"

RF_PARAMS = {
    "n_estimators": 100,
    "max_depth": None,
    "random_state": 42,
    "n_jobs": -1
}
