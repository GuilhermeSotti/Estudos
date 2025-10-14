from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("http_ingest")

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    logger.debug("python-dotenv não disponível ou .env não presente — ignora")

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", 5432))
PG_DB   = os.getenv("PG_DB", "factorydb")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASS = os.getenv("PG_PASS", "postgres")

DSN = f"host={PG_HOST} port={PG_PORT} dbname={PG_DB} user={PG_USER} password={PG_PASS}"

app = FastAPI(title="HTTP Ingest Service", version="1.0")

class IngestPayload(BaseModel):
    device_id: str
    ts: Optional[str] = None
    temp: float
    hum: float

    @validator("ts")
    def validate_ts(cls, v):
        if v is None:
            return v
        try:
            datetime.fromisoformat(v.replace("Z", "+00:00"))
            return v
        except Exception:
            raise ValueError("ts must be ISO8601 (ex: 2025-09-28T10:00:00Z)")

psycopg2 = None
_psycopg2_import_error = None
def _import_psycopg2():
    global psycopg2, _psycopg2_import_error
    if psycopg2 is not None or _psycopg2_import_error is not None:
        return
    try:
        import psycopg2
        from psycopg2.extras import execute_values
        psycopg2 = psycopg2
    except Exception as e:
        _psycopg2_import_error = e
        logger.warning("psycopg2 não disponível: %s", e)

def get_conn():
    _import_psycopg2()
    if _psycopg2_import_error is not None:
        raise RuntimeError(f"psycopg2 missing: {_psycopg2_import_error}")

    return psycopg2.connect(host=PG_HOST, port=PG_PORT, dbname=PG_DB, user=PG_USER, password=PG_PASS)

@app.on_event("startup")
def startup_event():

    try:
        _import_psycopg2()
        if _psycopg2_import_error:
            logger.warning("psycopg2 não encontrado — endpoints funcionarão, mas DB ficará indisponível até instalar a dependência.")
            return
        conn = get_conn()
        conn.close()
        logger.info("Conectividade com Postgres OK (host=%s db=%s)", PG_HOST, PG_DB)
    except Exception as e:
        logger.exception("Falha checando Postgres no startup: %s", e)

@app.get("/health")
def health():
    """Health check simples — tenta conectar ao DB e retorna status."""
    try:
        _import_psycopg2()
        if _psycopg2_import_error:
            return {"status": "ok", "db": False, "error": str(_psycopg2_import_error)}
        conn = get_conn()
        conn.close()
        return {"status": "ok", "db": True}
    except Exception as e:
        logger.exception("Health check DB falhou")
        return {"status": "ok", "db": False, "error": str(e)}

@app.post("/ingest", status_code=201)
def ingest(payload: IngestPayload):
    """Recebe JSON e grava em devices + measurements."""

    if payload.ts:
        try:
            ts = datetime.fromisoformat(payload.ts.replace("Z", "+00:00"))
        except Exception:
            ts = datetime.utcnow()
    else:
        ts = datetime.utcnow()

    try:
        conn = get_conn()
    except Exception as e:
        logger.exception("DB não disponível ao tentar inserir")
        raise HTTPException(status_code=503, detail=f"DB unavailable: {e}")

    try:
        cur = conn.cursor()

        cur.execute("INSERT INTO devices(device_id) VALUES (%s) ON CONFLICT (device_id) DO NOTHING;", (payload.device_id,))
        cur.execute(
            "INSERT INTO measurements(device_id, ts, temperature_c, humidity) VALUES (%s, %s, %s, %s)",
            (payload.device_id, ts, payload.temp, payload.hum)
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Inserted measurement device=%s ts=%s temp=%s hum=%s", payload.device_id, ts.isoformat(), payload.temp, payload.hum)
        return {"status": "ok", "device_id": payload.device_id, "ts": ts.isoformat()}
    except Exception as e:
        logger.exception("Erro ao inserir medida")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
