import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

def load_config(path: str = "config.yaml") -> str:
    """Carrega URI do banco de config.yaml na raíz do python_pipeline."""
    with open(path, 'r') as f:
        cfg = yaml.safe_load(f)
    uri = cfg.get('db_uri')
    if not uri:
        raise ValueError("db_uri não encontrado em config.yaml")
    return uri

def init_engine(uri: str):
    """Cria engine SQLAlchemy e inicializa tabelas."""
    engine = create_engine(uri, echo=False, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine=None):
    """Retorna uma sessão para operações CRUD."""
    if engine is None:
        uri = load_config()
        engine = init_engine(uri)
    Session = sessionmaker(bind=engine)
    return Session()
