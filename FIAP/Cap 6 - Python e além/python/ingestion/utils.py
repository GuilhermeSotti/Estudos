import yaml
import logging
import requests
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

def get_engine():
    cfg = load_config()["mssql"]
    DRIVER   = cfg["driver"]       
    SERVER   = cfg["host"]         
    DATABASE = cfg["database"]    
    odbc_str = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Timeout=30;"
        "Trusted_Connection=yes;"
    )
    connection_url = URL.create(
        "mssql+pyodbc",
        query={"odbc_connect": odbc_str}
    )
    engine = create_engine(connection_url)
    return engine

def load_config(path="Cap 6 - Python e além\python\config\config.yaml"):
    """Carrega configurações do projeto."""
    with open(path, "r") as f:
        return yaml.safe_load(f)

def get_logger(name=__name__):
    """Configura logger padrão."""
    cfg = load_config()["logging"]
    logging.basicConfig(
        filename=cfg["file"],
        level=cfg["level"],
        format=cfg["format"]
    )
    return logging.getLogger(name)

def sql_connection():
    cfg = load_config()["mssql"]
    DRIVER   = cfg["driver"]       
    SERVER   = cfg["host"]         
    DATABASE = cfg["database"]    
    odbc_str = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(odbc_str)

def fetch_json(url, params=None, timeout=30):
    """GET request e retorno de JSON."""
    resp = requests.get(url, params=params, timeout=timeout,verify=False   )
    resp.raise_for_status()
    return resp.json()
