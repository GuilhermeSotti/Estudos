import yaml
import json
import time
from serial import Serial, SerialException
from database.db import init_engine, get_session
from database.models import Sensor

def load_ingest_config(path: str = "Cap 1 - Automação e inteligência na FarmTech Solutions\python\database\config.yaml") -> dict:
    """Carrega portas e URI do ingest."""
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def main():
    cfg = load_ingest_config()
    serial_cfg = cfg['serial'] if 'serial' in cfg else {}
    port = serial_cfg.get('port', '/dev/ttyUSB0')
    baud = serial_cfg.get('baud_rate', 115200)
    
    engine = init_engine(cfg['db_uri'])
    session = get_session(engine)
    
    try:
        ser = Serial(port, baud, timeout=1)
        print(f"[Ingest] Conectado a {port} @ {baud}bps")
    except SerialException as e:
        print(f"[Erro] Não foi possível abrir {port}: {e}")
        return

    while True:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            time.sleep(0.1)
            continue
        try:
            data = json.loads(line)
            record = Sensor(
                umidade=float(data['umidade']),
                nutriente=float(data['nutriente'])
            )
            session.add(record)
            session.commit()
            print(f"[Ingest] Gravado: {record}")
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"[Warning] Linha inválida: {line} -> {e}")

if __name__ == "__main__":
    main()
