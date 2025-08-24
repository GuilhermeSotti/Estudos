# Consumidor MQTT que injeta leituras no PostgreSQL.
# Requisitos: paho-mqtt, psycopg2-binary, python-dotenv
#
# Uso:
# - Criar .env com variáveis (exemplo no README)
# - Executar: python mqtt_consumer.py
#
# O consumidor:
# - subscreve tópico (ex: factory/machine/+/sensors)
# - espera payload JSON com formato:
#   {"machine_id": "M1", "ts": "2025-08-13T12:01:00Z",
#    "sensors": [{"type":"vibration","value":0.51,"unit":"g"},
#                {"type":"temperature","value":42.1,"unit":"C"}]}
# - cria/atualiza metadados (machine, sensor) e insere leituras em lote

import os
import json
import time
import logging
import traceback
import signal
from threading import Thread, Event
from queue import Queue, Empty
from datetime import datetime
from typing import List, Tuple, Optional
import sqlite3
import paho.mqtt.client as mqtt

# Carregar .env se existir
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

USE_SQLITE = os.getenv("USE_SQLITE", "false").lower() in ("1", "true", "yes")

if not USE_SQLITE:
    try:
        import psycopg2
        from psycopg2.extras import execute_values
    except Exception:
        raise RuntimeError("psycopg2 não encontrado. Instale com: pip install psycopg2-binary")


MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "factory/machine/+/sensors")
MQTT_QOS = int(os.getenv("MQTT_QOS", "1"))

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_DB = os.getenv("PG_DB", "pm_db")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASS = os.getenv("PG_PASS", "postgres")

SQLITE_DB = os.getenv("SQLITE_DB", "pm_demo.db")

BATCH_SIZE = int(os.getenv("BATCH_SIZE", "256"))
BATCH_INTERVAL = float(os.getenv("BATCH_INTERVAL", "2.0"))  # segundos

LOG_LEVEL = os.getenv("ENV_LOG_LEVEL", "INFO").upper()

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("mqtt_consumer")


insert_queue: "Queue[Tuple]" = Queue()
stop_event = Event()

conn = None

def get_pg_conn():
    """Retorna uma conexão psycopg2 (nova)."""
    return psycopg2.connect(host=PG_HOST, port=PG_PORT, dbname=PG_DB, user=PG_USER, password=PG_PASS)

def ensure_schema_pg(conn):
    """Cria esquema básico se não existir."""
    ddl_path = os.path.join(os.path.dirname(__file__), "postgres_dump.sql")
    with open(ddl_path, "r", encoding="utf-8") as f:
            ddl = f.read()

    with conn.cursor() as cur:
        cur.execute(ddl)
    conn.commit()

def ensure_schema_sqlite(conn):
    """Cria esquema básico se não existir."""
    ddl_path = os.path.join(os.path.dirname(__file__), "sqlite_dump.sql")
    with open(ddl_path, "r", encoding="utf-8") as f:
            ddl = f.read()

    with conn.cursor() as cur:
        cur.execute(ddl)
    conn.commit()

def flush_buffer_pg(conn, items: List[Tuple[str, str, str, Optional[str], float]]):
    """
    items: lista de tuplas (machine_code, ts_iso, sensor_type, unit, value)
    Insere leituras em lote; faz upsert de máquina e sensor conforme necessário.
    """
    if not items:
        return
    with conn.cursor() as cur:
        machine_map = {}
        sensor_map = {}
        readings = []
        for machine_code, ts_iso, s_type, unit, val in items:
            if machine_code not in machine_map:
                cur.execute("SELECT machine_id FROM machine WHERE code=%s", (machine_code,))
                r = cur.fetchone()
                if r:
                    machine_map[machine_code] = r[0]
                else:
                    cur.execute("INSERT INTO machine(code) VALUES(%s) RETURNING machine_id", (machine_code,))
                    machine_map[machine_code] = cur.fetchone()[0]
            mid = machine_map[machine_code]
            s_key = (mid, s_type)
            if s_key not in sensor_map:
                cur.execute("SELECT sensor_id FROM sensor WHERE machine_id=%s AND type=%s", (mid, s_type))
                r = cur.fetchone()
                if r:
                    sensor_map[s_key] = r[0]
                else:
                    cur.execute("INSERT INTO sensor(machine_id,type,unit) VALUES(%s,%s,%s) RETURNING sensor_id", (mid, s_type, unit))
                    sensor_map[s_key] = cur.fetchone()[0]
            sid = sensor_map[s_key]
            try:
                ts_val = datetime.fromisoformat(ts_iso.replace("Z", "+00:00"))
            except Exception:
                ts_val = datetime.utcnow()
            readings.append((sid, ts_val, float(val)))
        execute_values(cur, "INSERT INTO reading (sensor_id, ts, value) VALUES %s", readings)
    conn.commit()
    log.debug("Flush PG: inseridas %d leituras", len(readings))

def get_sqlite_conn():
    c = sqlite3.connect(SQLITE_DB, check_same_thread=False)
    return c


def flush_buffer_sqlite(conn, items: List[Tuple[str, str, str, Optional[str], float]]):
    if not items:
        return
    cur = conn.cursor()
    machine_map = {}
    sensor_map = {}
    readings = []
    for machine_code, ts_iso, s_type, unit, val in items:
        if machine_code not in machine_map:
            cur.execute("SELECT machine_id FROM machine WHERE code=?", (machine_code,))
            r = cur.fetchone()
            if r:
                machine_map[machine_code] = r[0]
            else:
                cur.execute("INSERT INTO machine(code) VALUES(?)", (machine_code,))
                machine_map[machine_code] = cur.lastrowid
        mid = machine_map[machine_code]
        s_key = (mid, s_type)
        if s_key not in sensor_map:
            cur.execute("SELECT sensor_id FROM sensor WHERE machine_id=? AND type=?", (mid, s_type))
            r = cur.fetchone()
            if r:
                sensor_map[s_key] = r[0]
            else:
                cur.execute("INSERT INTO sensor(machine_id,type,unit) VALUES(?,?,?)", (mid, s_type, unit))
                sensor_map[s_key] = cur.lastrowid
        sid = sensor_map[s_key]
        try:
            datetime.fromisoformat(ts_iso.replace("Z", "+00:00"))
            ts_str = ts_iso
        except Exception:
            ts_str = datetime.utcnow().isoformat() + "Z"
        readings.append((sid, ts_str, float(val)))
    cur.executemany("INSERT INTO reading(sensor_id, ts, value) VALUES(?,?,?)", readings)
    conn.commit()
    log.debug("Flush SQLite: inseridas %d leituras", len(readings))


def batch_writer_worker():
    """
    Worker de background que consome insert_queue e faz flush em lote
    para o banco selecionado (Postgres ou SQLite).
    """
    global conn
    buffer = []
    last_flush = time.time()
    local_conn = None

    while not stop_event.is_set():
        try:
            item = insert_queue.get(timeout=BATCH_INTERVAL)
            if item == "__STOP__":
                if buffer:
                    try:
                        if USE_SQLITE:
                            if local_conn is None:
                                local_conn = get_sqlite_conn()
                                ensure_schema_sqlite(local_conn)
                            flush_buffer_sqlite(local_conn, buffer)
                        else:
                            if conn is None:
                                conn = get_pg_conn()
                                ensure_schema_pg(conn)
                            flush_buffer_pg(conn, buffer)
                        buffer = []
                    except Exception:
                        log.exception("Erro ao flush final no STOP:")
                break
            buffer.append(item)
        except Empty:
            pass
        except Exception:
            log.exception("Erro ao obter item da fila:")

        now = time.time()
        if len(buffer) >= BATCH_SIZE or (buffer and now - last_flush >= BATCH_INTERVAL):
            try:
                if USE_SQLITE:
                    if local_conn is None:
                        local_conn = get_sqlite_conn()
                        ensure_schema_sqlite(local_conn)
                    flush_buffer_sqlite(local_conn, buffer)
                else:
                    if conn is None:
                        conn = get_pg_conn()
                        ensure_schema_pg(conn)
                    flush_buffer_pg(conn, buffer)
                buffer = []
                last_flush = now
            except Exception:
                log.exception("Erro ao inserir batch — manter buffer e tentar novamente")
                time.sleep(1)

    try:
        if local_conn:
            local_conn.close()
    except:
        pass
    log.info("Batch writer finalizado.")

def on_connect(client, userdata, flags, rc, properties=None):
    log.info("Conectado ao broker MQTT (rc=%s). Subscrevendo: %s", rc, MQTT_TOPIC)
    try:
        client.subscribe(MQTT_TOPIC, qos=MQTT_QOS)
    except Exception:
        log.exception("Erro ao subscrever tópico %s", MQTT_TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8", errors="replace")
    log.debug("Mensagem recebida em %s: %s", msg.topic, payload[:200])
    try:
        data = json.loads(payload)
    except Exception:
        try:
            val = float(payload.strip())
            data = {"machine_id": "1", "timestamp": datetime.utcnow().isoformat() + "Z", "sensors":[{"type": msg.topic.split("/")[-1], "value": val}]}
        except Exception:
            log.error("Payload JSON inválido e não foi possível interpretar: %s", payload)
            return

    machine = data.get("machine_id") or data.get("machine") or "MACHINE_DEFAULT"
    ts = data.get("timestamp") or data.get("ts") or datetime.utcnow().isoformat() + "Z"

    sensors = data.get("sensors")
    if sensors and isinstance(sensors, list):
        for s in sensors:
            s_type = s.get("type") or s.get("sensor_type") or "unknown"
            unit = s.get("unit")
            val = s.get("value")
            if val is None:
                continue
            try:
                numeric_val = float(val)
            except Exception:
                log.debug("Valor do sensor não numérico: %s", val)
                continue
            insert_queue.put((machine, ts, s_type, unit, numeric_val))
    else:
        for key in ("vibration","temperature","current"):
            if key in data:
                try:
                    numeric_val = float(data[key])
                    insert_queue.put((machine, ts, key, None, numeric_val))
                except Exception:
                    continue

def connect_with_backoff(client: mqtt.Client, host: str, port: int, max_retries: int = 0):
    """Tenta conectar com backoff exponencial. max_retries=0 -> infinito."""
    attempt = 0
    while not stop_event.is_set():
        try:
            client.connect(host, port, 60)
            log.info("Conectado ao broker MQTT %s:%s", host, port)
            return
        except Exception as e:
            attempt += 1
            wait = min(2 ** attempt, 30)
            log.warning("Falha ao conectar MQTT (tentativa %d): %s — aguardando %ds", attempt, e, wait)
            time.sleep(wait)
            if max_retries and attempt >= max_retries:
                log.error("Excedeu max_retries ao conectar MQTT")
                raise

def signal_handler(sig, frame):
    log.info("Sinal recebido (%s). Iniciando shutdown...", sig)
    stop_event.set()
    insert_queue.put("__STOP__")


def main():
    global conn
    writer = Thread(target=batch_writer_worker, daemon=True)
    writer.start()

    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        connect_with_backoff(client, MQTT_BROKER, MQTT_PORT)
    except Exception:
        log.exception("Não foi possível conectar ao broker MQTT, saindo.")
        stop_event.set()
        insert_queue.put("__STOP__")
        writer.join(timeout=5)
        return

    client.loop_start()

    try:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    except Exception:
        log.debug("Registro de sinais: plataforma pode não suportar todos os sinais.")

    log.info("mqtt_consumer pronto. Aguarde mensagens... (Ctrl+C para sair)")

    try:
        while not stop_event.is_set():
            time.sleep(1)
            if not writer.is_alive():
                log.error("Thread de escrita ao DB parou inesperadamente. Reiniciando thread.")
                writer = Thread(target=batch_writer_worker, daemon=True)
                writer.start()
    except Exception:
        log.exception("Erro inesperado no loop principal:")
    finally:
        log.info("Shutdown: sinalizando writer e aguardando flush")
        try:
            insert_queue.put("__STOP__")
            writer.join(timeout=10)
        except Exception:
            log.exception("Erro aguardando fim do writer")
        try:
            client.loop_stop()
            client.disconnect()
        except Exception:
            pass
        if conn:
            try:
                conn.close()
            except Exception:
                pass
        log.info("Encerrado mqtt_consumer.")

if __name__ == "__main__":
    main()