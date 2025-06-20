import logging
import os

def setup_logging(log_dir: str, level: str = "INFO"):
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "run.log")
    logger = logging.getLogger()
    logger.setLevel(level)
    # handler para console
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s:%(name)s: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # handler para arquivo
    fh = logging.FileHandler(log_path)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
