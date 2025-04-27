import time
from datetime import datetime

from config import SERIAL_PORT, BAUD_RATE
from serial_reader import SerialReader
from db.crud import insert_reading
from weather.service import fetch_weather

def main():
    sr = SerialReader(SERIAL_PORT, BAUD_RATE)

    while True:
        payload = sr.read_json()
        if payload:
            ts = datetime.now()
            sensors = payload.get("sensors", {})
            mapping = {
                1: "pH",
                2: "humidity",
                3: "P",
                4: "K"
            }
            for sid, key in mapping.items():
                if key in sensors:
                    insert_reading(
                        sensor_id=sid,
                        valor=float(sensors[key]),
                        historico_id=1,
                        timestamp=ts
                    )

            if fetch_weather():
                print(f"{ts} – Previsão de chuva, irrigação pulada.")

        time.sleep(5)

if __name__ == "__main__":
    main()
