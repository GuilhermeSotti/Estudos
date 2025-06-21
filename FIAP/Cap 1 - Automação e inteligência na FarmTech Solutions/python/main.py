import yaml
import json
import time
import serial
from database.db import init_engine, get_session
from database.models import Reading

def load_ingest_config(path: str) -> dict:
    """Carrega configurações do arquivo config.yaml."""
    with open(path, 'r') as f:
        cfg = yaml.safe_load(f)
    return cfg

def main():
    cfg = load_ingest_config(path="Cap 1 - Automação e inteligência na FarmTech Solutions/python/config.yaml")
    serial_cfg = cfg.get('serial', {})
    port = serial_cfg.get('port', 'rfc2217://localhost:4000')
    baud = serial_cfg.get('baud_rate', 115200)

    engine = init_engine(cfg['db_uri'])
    session = get_session(engine)

    try:
        ser = serial.serial_for_url(port, baudrate=baud, timeout=1)
        print(f"[Ingest] Conectado a {port} @ {baud}bps")
    except Exception as e:
        print(f"[Erro] Não foi possível abrir {port}: {e}")
        return

    while True:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            time.sleep(0.1); continue
        try:
            data = json.loads(line)
            umid = float(data['umidade']); nutr = float(data['nutriente'])
            record = Reading(umidade=umid, nutriente=nutr)
            session.add(record); session.commit()
            print(f"[Ingest] Gravado: {record}")
        except Exception as e:
            session.rollback()
            print(f"[Warning] {line} -> {e}")

if __name__ == "__main__":
    main()
